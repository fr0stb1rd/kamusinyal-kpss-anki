# KamuSinyal 2026 KPSS Anki Desteleri

Bu depo, **KamuSinyal** ekosisteminin bir parçası olarak geliştirilen, KPSS (Kamu Personeli Seçme Sınavı) hazırlık sürecine yönelik modern ve modüler Anki kartlarını içerir. KamuSinyal projesinin eğitim materyalleri bacağını desteklemek amacıyla oluşturulmuş bir alt kaynaktır.

## Özellikler
- **5 Ana Ders**: Tarih, Türkçe, Matematik, Vatandaşlık, Coğrafya.
- **Yalın Tasarım**: Anki'nin yerel gece ve gündüz modlarıyla tam uyumlu, göz yormayan minimalist tasarım.
- **Kolay Yönetim**: Kartlar tamamen `.txt` dosyaları üzerinden yönetilir; teknik bilgi gerektirmeden soru eklenebilir.

## Nasıl Kullanılır?

1. **Desteleri İndirin:** [KamuSinyal KPSS Anki En Son Sürüm (Releases)](https://github.com/fr0stb1rd/kamusinyal-kpss-anki/releases/latest) sayfasına gidin ve indirmek istediğiniz derslerin `.apkg` dosyalarını bilgisayarınıza veya telefonunuza indirin.
2. **Anki'ye Aktarın:** `.apkg` formatındaki bir desteyi Anki'ye içe aktarmak, Anki'deki en kolay ve en sorunsuz aktarım işlemidir. Bu dosya türü kartları, çalışma geçmişinizi ve içindeki tüm medya (ses, resim) dosyalarını tek seferde yükler.

Kullandığınız cihaza göre aşağıdaki adımları sırasıyla uygulayabilirsiniz:

### 💻 1. Masaüstü Bilgisayar (Windows / Mac / Linux)
Bilgisayarda bu işlemi yapmanın en pratik yolu çift tıklamaktır.

*   **1. Yöntem (En Kolay):**
    İndirdiğiniz `.apkg` dosyasına bilgisayarınızda çift tıklayın. Anki otomatik olarak açılacak ve desteyi içeri aktaracaktır.
*   **2. Yöntem (Program İçinden):**
    1. Anki programını açın.
    2. Sol üstteki **Dosya (File)** menüsüne tıklayın.
    3. **İçe Aktar (Import)** seçeneğine tıklayın (Kısayol: `Ctrl + I`).
    4. Açılan pencerede `.apkg` dosyanızı bulun, seçin ve **Aç (Open)** butonuna basın.

    > **Sonuç:** Ekranda *"X adet not eklendi"* şeklinde bir başarı raporu göreceksiniz. Desteniz ana ekrana eklenecektir.

### 📱 2. Android Telefon (AnkiDroid)
Android cihazlarda güvenli aktarım için uygulama içindeki menüyü kullanmak en sağlıklı yöntemdir.

1. [**AnkiDroid**](https://play.google.com/store/apps/details?id=com.ichi2.anki) uygulamasını açın.
2. Sağ üst köşede bulunan **üç nokta (Menü)** simgesine dokunun.
3. **Desteyi içe aktar (Import deck)** seçeneğini seçin.
4. Telefonunuzun dosya yöneticisi açılacaktır. Buradan indirdiğiniz `.apkg` dosyasını bulun ve üzerine dokunun.
5. Uygulama dosyayı işleyecek ve *"İçe aktarma başarılı"* uyarısı verecektir.

### 🍏 3. iPhone / iPad (AnkiMobile)
iOS işletim sisteminde aktarım Apple'ın **"Paylaş"** menüsü üzerinden yapılır.

1. Telefonunuzdaki **Dosyalar (Files)** uygulamasını açın ve `.apkg` dosyasını bulun.
2. Dosyanın üzerine basılı tutun ve **Paylaş (Share)** seçeneğine dokunun.
3. Uygulama listesinden [**AnkiMobile**](https://apps.apple.com/tr/app/ankimobile-flashcards/id373493387) uygulamasını seçin.
4. Anki otomatik olarak açılacak ve desteyi koleksiyonunuza ekleyecektir.

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

## Lisans
Bu proje, [MIT](https://github.com/fr0stb1rd/kamusinyal-kpss-anki/blob/main/LICENSE) lisansı altında dağıtılmaktadır.
