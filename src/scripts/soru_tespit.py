#!/usr/bin/env python3
"""
soru_tespit.py
Scans raw_data/*.txt files for lines containing more than one '?' mark.
If any such lines are found, lists their line numbers and contents,
and exits with code 1 to halt CI workflows.
Otherwise, exits with 0.

Usage:
  python scripts/soru_tespit.py                 # scans all raw_data/*.txt
  python scripts/soru_tespit.py raw_data/cografya.txt
"""

import sys
import os

RAW_DIR = "src/raw_data"


def scan_file(file_path: str) -> int:
    """
    Scans a single file and prints lines with >1 question marks.
    Returns the count of detected malformed lines.
    """
    if not os.path.exists(file_path):
        print(f"❌ Dosya bulunamadı: {file_path}")
        return 0

    print(f"🔍 Dosya taranıyor: {file_path}")
    print("=" * 70)

    count = 0
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1254']
    lines = None

    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if lines is None:
        print(f"❌ Hata: Dosya kodlaması çözümlenemedi: {file_path}")
        return 0

    for line_no, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue

        q_count = line.count('?')
        if q_count > 1:
            count += 1
            print(f"📍 Satır {line_no:<4} | ({q_count} adet '?') ➔ {line}")

    if count == 0:
        print("   ✅ Bu dosya tamamen temiz.")
    print("=" * 70)
    return count


def main():
    targets = sys.argv[1:]

    # Default to scanning everything in raw_data if no args provided
    if not targets:
        if os.path.exists(RAW_DIR):
            targets = [
                os.path.join(RAW_DIR, f)
                for f in os.listdir(RAW_DIR)
                if f.endswith(".txt")
            ]
        else:
            print(f"❌ Hata: '{RAW_DIR}' klasörü bulunamadı.")
            sys.exit(1)

    if not targets:
        print("⚠️ Taranacak hiçbir .txt dosyası bulunamadı.")
        sys.exit(0)

    total_malformed = 0
    print("📊 Kalite Kontrol (QA) Taraması Başlıyor...")

    for path in targets:
        total_malformed += scan_file(path)

    print("\n📊 TARAMA SONUCU:")
    print(f"   • Sorunlu Satır Sayısı: {total_malformed}")

    if total_malformed > 0:
        print("\n❌ HATA: Çoklu soru işareti içeren satırlar tespit edildi!")
        print("💡 Lütfen yukarıdaki satırları 'scripts/soru_duzelt.py' ile veya elinizle düzeltin.")
        sys.exit(1)
    else:
        print("\n🎉 Tebrikler! Tüm dosyalar tertemiz. Build işlemine geçilebilir.")
        sys.exit(0)


if __name__ == "__main__":
    main()
