# KamuSinyal 2026 KPSS Anki Desteleri

Bu depo, **KamuSinyal** ekosisteminin bir parçası olarak geliştirilen, KPSS (Kamu Personeli Seçme Sınavı) hazırlık sürecine yönelik modern ve modüler Anki kartlarını içerir. KamuSinyal projesinin eğitim materyalleri bacağını desteklemek amacıyla oluşturulmuş bir alt kaynaktır.

## Özellikler
- **5 Ana Ders**: Tarih, Türkçe, Matematik, Vatandaşlık, Coğrafya.
- **50 Temel Soru**: Başlangıç seviyesi için her dersten 10 adet özenle seçilmiş soru.
- **Premium Tasarım**: KamuSinyal görsel kimliğine uygun, modern renk paleti ve ders bazlı kodlama.
- **Brain Brew Altyapısı**: Kartlar tamamen metin tabanlı (CSV) dosyalar üzerinden yönetilir ve teknik kullanıcılar için kolayca genişletilebilir.

## Deste Yapısı
Desteler `build/` klasörü altında, KamuSinyal markasıyla uyumlu paketler halinde sunulmaktadır:
- `build/KamuSinyal 2026 KPSS Tüm Dersler` (Kapsamlı Master Deste)
- `build/KamuSinyal 2026 KPSS Tarih`
- `build/KamuSinyal 2026 KPSS Türkçe`
- `build/KamuSinyal 2026 KPSS Matematik`
- `build/KamuSinyal 2026 KPSS Vatandaşlık`
- `build/KamuSinyal 2026 KPSS Coğrafya`

## Kurulum ve Kullanım
1. Bilgisayarınızda Anki yüklü olduğundan emin olun.
2. Anki'ye **CrowdAnki** (Eklenti Kodu: `1788670778`) eklentisini kurun.
3. Anki menüsünden `File -> CrowdAnki: Import from disk` yolunu izleyin.
4. Bu depodaki `build/` klasörü içinden aktarmak istediğiniz dersin klasörünü seçin.

## Geliştirme Süreci
Bu repo, KamuSinyal içeriklerinin en kolay şekilde yönetilmesi için tasarlanmıştır. Veri eklemek için:

1. `src/raw_data/` altındaki ilgili dersin `.csv` dosyasını düzenleyin. Sadece `guid`, `Question` ve `Answer` alanlarını doldurmanız yeterlidir.
2. Aşağıdaki komutu çalıştırarak verileri genişletin (bu komut ders isimlerini ve etiketleri otomatik ekler):
```bash
python3 scripts/expand_data.py
```
3. Desteleri inşa edin:
```bash
./venv/bin/brain-brew run recipes/kpss.yaml
```

---
**KamuSinyal** hakkında daha fazla bilgi ve diğer projeler için ana proje sayfasını ziyaret edebilirsiniz.
