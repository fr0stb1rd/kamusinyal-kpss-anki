#!/usr/bin/env python3
"""
crowdanki_to_apkg.py
Converts build/*/deck.json (CrowdAnki format) to build/*.apkg files
using the genanki library.
"""

import json
import os
import sys
import re
import hashlib
import genanki

BUILD_DIR = "build"

# CSS for the cards (mirrors src/note_models/kpss.css)
CARD_CSS = """
.card {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 18px;
    text-align: center;
    color: #222;
    padding: 20px;
    line-height: 1.6;
}
.small-footer {
    color: #aaa;
    font-size: 12px;
    margin-top: 16px;
}
"""

# Front / Back templates
FRONT_TMPL = "{{Question}}"
BACK_TMPL = """{{FrontSide}}
<hr id="answer">
{{Answer}}
<br><br>
<div class="small-footer">KamuSinyal 2026 KPSS Anki</div>"""


def stable_id(name: str, salt: str = "kpss-anki-2026") -> int:
    """Generate a stable integer ID from a string (fits in Anki's int range)."""
    h = hashlib.sha256(f"{salt}:{name}".encode()).hexdigest()
    return int(h[:8], 16) % (2**31 - 1)


def load_deck_json(folder: str) -> dict:
    path = os.path.join(folder, "deck.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_notes_from_deck(deck: dict) -> list[dict]:
    """Recursively collect all notes from a deck (and its children)."""
    notes = list(deck.get("notes", []))
    for child in deck.get("children", []):
        notes.extend(get_notes_from_deck(child))
    return notes


def build_apkg(folder: str) -> str:
    """Convert a single deck folder to an .apkg file. Returns output path."""
    data = load_deck_json(folder)
    deck_name = data.get("name", os.path.basename(folder))

    # Build genanki model
    model_id = stable_id(f"model:{deck_name}")
    model = genanki.Model(
        model_id,
        "KPSS Soru-Cevap",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Soru-Cevap",
                "qfmt": FRONT_TMPL,
                "afmt": BACK_TMPL,
            }
        ],
        css=CARD_CSS,
    )

    # Build genanki deck
    deck_id = stable_id(f"deck:{deck_name}")
    deck = genanki.Deck(deck_id, deck_name)

    # Collect all notes
    raw_notes = get_notes_from_deck(data)
    skipped = 0
    for raw in raw_notes:
        fields = raw.get("fields", [])
        if len(fields) < 2:
            skipped += 1
            continue
        question, answer = fields[0], fields[1]
        tags = raw.get("tags", [])

        note = genanki.Note(
            model=model,
            fields=[question, answer],
            tags=tags,
            guid=genanki.guid_for(raw.get("guid", question)),
        )
        deck.add_note(note)

    if skipped:
        print(f"     ⚠️  {skipped} not atlandı (eksik alan).")

    # Output path: build/<deck_name>.apkg
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", deck_name)
    out_path = os.path.join(BUILD_DIR, f"{safe_name}.apkg")

    pkg = genanki.Package(deck)
    pkg.write_to_file(out_path)
    return out_path


def main():
    # 1. Clean existing .apkg files to prevent obsolete releases
    if os.path.exists(BUILD_DIR):
        for f in os.listdir(BUILD_DIR):
            if f.endswith(".apkg"):
                try:
                    os.remove(os.path.join(BUILD_DIR, f))
                except Exception as e:
                    print(f"⚠️ Eski apkg temizlenemedi: {e}")

    targets = sys.argv[1:]

    if not targets:
        # Tüm build/ alt klasörlerini işle
        targets = [
            os.path.join(BUILD_DIR, d)
            for d in os.listdir(BUILD_DIR)
            if os.path.isdir(os.path.join(BUILD_DIR, d))
               and os.path.exists(os.path.join(BUILD_DIR, d, "deck.json"))
        ]

    if not targets:
        print("❌ Hiç deck.json bulunmuş klasör yok. Önce brain-brew çalıştır.")
        sys.exit(1)

    print(f"📦 {len(targets)} deste için .apkg üretimi başlıyor...")
    for folder in targets:
        deck_name = os.path.basename(folder)
        print(f"  🃏 {deck_name}")
        try:
            out = build_apkg(folder)
            count = len(get_notes_from_deck(load_deck_json(folder)))
            print(f"     ✅ {count} kart → {out}")
        except Exception as e:
            print(f"     ❌ Hata: {e}")

    print("✅ Tamamlandı.")


if __name__ == "__main__":
    main()
