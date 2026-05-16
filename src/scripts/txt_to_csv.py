#!/usr/bin/env python3
"""
txt_to_csv.py
Converts raw_data/*.txt files to src/data/*.csv files, clears unused CSV files,
and dynamically generates the brain-brew recipe 'recipes/kpss.yaml' based on
only the available raw text files.

Usage:
  python scripts/txt_to_csv.py                 # processes all raw_data/*.txt
"""

import csv
import os
import sys

# Full map of supported courses and their metadata
COURSE_METADATA = {
    "cografya": {
        "csv": "cografya.csv",
        "guid_prefix": "cog",
        "tag": "KPSS::Cografya",
        "name_tr": "Coğrafya",
        "uuid": "kpss-cografya-v8"
    },
    "tarih": {
        "csv": "tarih.csv",
        "guid_prefix": "tar",
        "tag": "KPSS::Tarih",
        "name_tr": "Tarih",
        "uuid": "kpss-tarih-v8"
    },
    "turkce": {
        "csv": "turkce.csv",
        "guid_prefix": "trk",
        "tag": "KPSS::Turkce",
        "name_tr": "Türkçe",
        "uuid": "kpss-turkce-v8"
    },
    "matematik": {
        "csv": "matematik.csv",
        "guid_prefix": "mat",
        "tag": "KPSS::Matematik",
        "name_tr": "Matematik",
        "uuid": "kpss-matematik-v8"
    },
    "vatandaslik": {
        "csv": "vatandaslik.csv",
        "guid_prefix": "vat",
        "tag": "KPSS::Vatandaslik",
        "name_tr": "Vatandaşlık",
        "uuid": "kpss-vatandaslik-v8"
    },
}

RAW_DIR = "src/raw_data"
CSV_DIR = "src/data"
RECIPE_PATH = "src/recipes/kpss.yaml"


def parse_txt(path: str, guid_prefix: str, tag: str) -> list[dict]:
    """Read a txt file and return a list of note dicts."""
    rows = []
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1254"]

    lines = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if lines is None:
        print(f"  ❌ Kodlama hatası: {path}")
        return rows

    note_counter = 0
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # First '?' splits question and answer
        idx = line.find("?")
        if idx == -1:
            continue  # skip comments / headers

        question = line[: idx + 1].strip()
        answer = line[idx + 1 :].strip()

        if not question or not answer:
            continue

        note_counter += 1
        guid = f"{guid_prefix}-{note_counter}"

        rows.append({
            "guid": guid,
            "Question": question,
            "Answer": answer,
            "tags": tag,
        })

    return rows


def write_csv(rows: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["guid", "Question", "Answer", "tags"])
        writer.writeheader()
        writer.writerows(rows)


def generate_yaml_recipe(active_stems: list[str]) -> None:
    """Generate brain-brew recipe dynamically based on active stems."""
    yaml_lines = [
        "- build_parts:",
        "  - note_model_from_yaml_part: { part_id: kpss_model, file: src/note_models/kpss.yaml }",
        "",
        "  - headers_from_yaml_part:",
        "      - part_id: header_master",
        "        file: src/headers/kpss_default.yaml",
        '        override: { name: "KamuSinyal 2026 KPSS Tüm Dersler", crowdanki_uuid: "kpss-master-v8", deck_description_html_file: "src/headers/kpss_desc.html" }'
    ]

    # Add header parts for each course
    for stem in active_stems:
        meta = COURSE_METADATA[stem]
        name_tr = meta["name_tr"]
        uuid = meta["uuid"]
        yaml_lines.append(f"      - part_id: header_{stem}")
        yaml_lines.append("        file: src/headers/kpss_default.yaml")
        yaml_lines.append(f'        override: {{ name: "KamuSinyal 2026 KPSS {name_tr}", crowdanki_uuid: "{uuid}", deck_description_html_file: "src/headers/kpss_desc.html" }}')

    yaml_lines.append("")

    # Add notes_from_csvs parts for each course
    for stem in active_stems:
        meta = COURSE_METADATA[stem]
        csv_file = f"src/data/{meta['csv']}"
        yaml_lines.extend([
            "  - notes_from_csvs:",
            f"      part_id: {stem}_notes",
            "      note_model_mappings: [{ note_models: [kpss_model], columns_to_fields: { guid: guid, tags: tags, Question: Question, Answer: Answer } }]",
            f"      file_mappings: [{{ file: {csv_file}, note_model: kpss_model }}]",
            ""
        ])

    # Add notes_from_csvs part for master (all combined)
    yaml_lines.extend([
        "  - notes_from_csvs:",
        "      part_id: master_notes",
        "      note_model_mappings: [{ note_models: [kpss_model], columns_to_fields: { guid: guid, tags: tags, Question: Question, Answer: Answer } }]",
        "      file_mappings:"
    ])
    for stem in active_stems:
        meta = COURSE_METADATA[stem]
        csv_file = f"src/data/{meta['csv']}"
        yaml_lines.append(f"        - {{ file: {csv_file}, note_model: kpss_model }}")

    yaml_lines.append("")

    # Generate crowd_anki generators
    yaml_lines.append('- generate_crowd_anki: { folder: "build/KamuSinyal 2026 KPSS Tüm Dersler", headers: header_master, note_models: { parts: [{ part_id: kpss_model }] }, notes: { part_id: master_notes } }')
    for stem in active_stems:
        yaml_lines.append(f'- generate_crowd_anki: {{ folder: "build/KamuSinyal 2026 KPSS {COURSE_METADATA[stem]["name_tr"]}", headers: header_{stem}, note_models: {{ parts: [{{ part_id: kpss_model }}] }}, notes: {{ part_id: {stem}_notes }} }}')
    yaml_lines.append("")

    # Write recipe
    os.makedirs(os.path.dirname(RECIPE_PATH), exist_ok=True)
    with open(RECIPE_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))
    print(f"  📝 {RECIPE_PATH} başarıyla güncellendi ({len(active_stems)} ders dahil edildi).")


def main():
    print("🔄 raw_data → src/data dönüşümü ve mimari temizlik başlıyor...")

    # Determine active stems based on raw_data/*.txt files that exist
    if not os.path.exists(RAW_DIR):
        print(f"❌ {RAW_DIR} klasörü bulunamadı.")
        sys.exit(1)

    active_stems = []
    for f in os.listdir(RAW_DIR):
        if f.endswith(".txt"):
            stem = os.path.splitext(f)[0]
            if stem in COURSE_METADATA:
                active_stems.append(stem)

    if not active_stems:
        print("⚠️ raw_data klasöründe aktif hiçbir .txt dosyası bulunamadı.")
        sys.exit(0)

    # 1. Process active stems
    for stem in active_stems:
        meta = COURSE_METADATA[stem]
        txt_path = os.path.join(RAW_DIR, f"{stem}.txt")
        csv_path = os.path.join(CSV_DIR, meta["csv"])

        print(f"  📄 {txt_path}  →  {csv_path}")
        rows = parse_txt(txt_path, meta["guid_prefix"], meta["tag"])
        write_csv(rows, csv_path)
        print(f"     ✅ {len(rows)} satır yazıldı.")

    # 2. Delete any CSV files in src/data that DO NOT have a corresponding .txt file
    if os.path.exists(CSV_DIR):
        for f in os.listdir(CSV_DIR):
            if f.endswith(".csv"):
                csv_stem = os.path.splitext(f)[0]
                # If there's no corresponding txt in raw_data, remove it
                if csv_stem not in active_stems and csv_stem in COURSE_METADATA:
                    csv_path = os.path.join(CSV_DIR, f)
                    print(f"  🧹 Temizleniyor (aktif txt yok): {csv_path}")
                    try:
                        os.remove(csv_path)
                    except Exception as e:
                        print(f"     ⚠️ Dosya silinemedi: {e}")

    # 3. Dynamically generate the recipe file kpss.yaml
    generate_yaml_recipe(active_stems)

    print("✅ Dönüşüm ve mimari temizlik tamamlandı.")


if __name__ == "__main__":
    main()
