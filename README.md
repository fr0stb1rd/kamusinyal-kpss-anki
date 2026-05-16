# KamuSinyal 2026 KPSS Anki Desteleri

Bu depo, **KamuSinyal** ekosisteminin bir parçası olarak geliştirilen, KPSS (Kamu Personeli Seçme Sınavı) hazırlık sürecine yönelik modern ve modüler Anki kartlarını içerir. KamuSinyal projesinin eğitim materyalleri bacağını desteklemek amacıyla oluşturulmuş bir alt kaynaktır.

## Özellikler
- **5 Ana Ders**: Tarih, Türkçe, Matematik, Vatandaşlık, Coğrafya.
- **Yalın Tasarım**: Anki'nin yerel gece ve gündüz modlarıyla tam uyumlu, göz yormayan minimalist tasarım.
- **Kolay Yönetim**: Kartlar tamamen `.txt` dosyaları üzerinden yönetilir; teknik bilgi gerektirmeden soru eklenebilir.

## Proje Mimarisi

Tüm kaynak kodları, ham metin verileri, derleme tarifleri ve yardımcı betikler tek bir düzenli yapı altında **`src/`** klasöründe birleştirilmiştir.

```
kamusinyal-kpss-anki/
├── src/                    ← Tüm Proje Kaynakları
│   ├── brain_brew_config.yaml ← Brain Brew ayar dosyası
│   ├── raw_data/           ← Ham kaynak metin dosyaları (Tek düzenleme noktası!)
│   │   └── cografya.txt
│   │
│   ├── data/               ← Üretilmiş geçici CSV'ler (gitignored)
│   │
│   ├── headers/            ← Deste meta verileri (isim, UUID, kart ayarları)
│   │   ├── kpss_default.yaml
│   │   └── kpss_desc.html
│   │
│   ├── note_models/        ← Kart tasarımı (CSS + HTML şablonu)
│   │   ├── kpss.css
│   │   ├── kpss.yaml
│   │   └── templates/
│   │       └── kpss_template.html
│   │
│   ├── recipes/            ← Brain Brew tarifleri (Dinamik üretilir)
│   │   └── kpss.yaml
│   │
│   └── scripts/            ← Otomasyon ve Yardımcı Betikler
│       ├── txt_to_csv.py   ← raw_data/*.txt → src/data/*.csv ve kpss.yaml üretimi
│       ├── crowdanki_to_apkg.py ← build/*/deck.json → build/*.apkg
│       ├── soru_tespit.py  ← Hatalı / çoklu soru işareti kontrolü (CI/CD test adımı)
│       └── soru_duzelt.py  ← Hatalı soru işaretlerini otomatik düzeltme
│
├── build/                  ← Üretilen CrowdAnki desteleri ve .apkg dosyaları (gitignored)
│   ├── KamuSinyal 2026 KPSS Coğrafya.apkg
│   └── ...
│
├── .github/workflows/
│   └── release.yml         ← Otomatik kalite testi, derleme ve GitHub Release
│
├── anki-manual-main/       ← Sadece yerelde saklanan referans dokümanları (gitignored)
└── README.md
```

---

## Build Pipeline (Derleme Akışı)

Her tag push yapıldığında veya yerelde derleme alındığında akış şu şekilde işler:

```
src/raw_data/*.txt
    │  src/scripts/soru_tespit.py (Kalite Kontrolü - Birden fazla '?' varsa DURDURUR)
    ▼
src/raw_data/*.txt  →  src/data/*.csv (txt_to_csv.py ile dinamik derleme)
    │  brain-brew run src/recipes/kpss.yaml
    ▼
build/*/deck.json (CrowdAnki Formatı)
    │  src/scripts/crowdanki_to_apkg.py
    ▼
build/*.apkg  →  GitHub Release / Anki Import'a Hazır!
```

---

## Yeni Soru Ekleme

Tek yapılması gereken ilgili **`src/raw_data/*.txt`** dosyasını düzenlemektir.

**Format:**
```
Soru metni buraya yazılır? Cevap metni buraya yazılır. (Opsiyonel hoca notu)
```

**Kural:** Satırdaki **ilk `?` işareti** soruyu cevaptan ayırır. Bir satırda birden fazla `?` işareti olamaz (olursa CI/CD aşamasında testler başarısız olur ve derleme durur).

---

## Yerel Derleme Alma

İlk kurulumda bağımlılıkları yükleyin:
```bash
python3 -m venv venv
./venv/bin/pip install brain-brew genanki
```

Ardından tüm adımları tek komutla çalıştırın:
```bash
python3 src/scripts/soru_tespit.py && python3 src/scripts/txt_to_csv.py && ./venv/bin/brain-brew run src/recipes/kpss.yaml && python3 src/scripts/crowdanki_to_apkg.py
```

Derlenen `.apkg` dosyalarınız saniyeler içinde **`build/`** klasöründe hazır olacaktır!
