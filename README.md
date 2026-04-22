# KamuSinyal 2026 KPSS Anki Desteleri

Bu depo, **KamuSinyal** ekosisteminin bir parçası olarak geliştirilen, KPSS (Kamu Personeli Seçme Sınavı) hazırlık sürecine yönelik modern ve modüler Anki kartlarını içerir. KamuSinyal projesinin eğitim materyalleri bacağını desteklemek amacıyla oluşturulmuş bir alt kaynaktır.

## Özellikler
- **5 Ana Ders**: Tarih, Türkçe, Matematik, Vatandaşlık, Coğrafya.
- **Yalın Tasarım**: Anki'nin yerel gece ve gündüz modlarıyla tam uyumlu, göz yormayan minimalist tasarım.
- **Kolay Yönetim**: Kartlar tamamen CSV dosyaları üzerinden yönetilir; teknik bilgi gerektirmeden soru eklenebilir.
- **Brain Brew Altyapısı**: Otomatik inşa sistemi sayesinde tek komutla tüm branş desteleri üretilir.

## Deste Yapısı
Desteler `build/` klasörü altında, branş bazlı ve toplu paketler halinde sunulmaktadır:
- `build/KamuSinyal 2026 KPSS Tüm Dersler` (Tüm Dersler Destesi)
- `build/KamuSinyal 2026 KPSS Tarih` (Tarih Destesi)
- `build/KamuSinyal 2026 KPSS Türkçe` (Türkçe Destesi)
- `build/KamuSinyal 2026 KPSS Matematik` (Matematik Destesi)
- `build/KamuSinyal 2026 KPSS Vatandaşlık` (Vatandaşlık Destesi)
- `build/KamuSinyal 2026 KPSS Coğrafya` (Coğrafya Destesi)

## Kurulum ve Kullanım
1. Bilgisayarınızda Anki yüklü olduğundan emin olun.
2. Anki'ye **CrowdAnki** (Eklenti Kodu: `1788670778`) eklentisini kurun.
3. Anki menüsünden `File -> CrowdAnki: Import from disk` yolunu izleyin.
4. Bu depodaki `build/` klasörü içinden aktarmak istediğiniz dersin klasörünü seçin.

## Geliştirme Süreci (Yeni Soru Ekleme)
Bu depo, KamuSinyal içeriklerinin en kolay şekilde yönetilmesi için tasarlanmıştır. Yeni bir soru eklemek için sadece şu adımları izleyin:

1. `src/data/` altındaki ilgili dersin `.csv` dosyasını (örneğin `tarih.csv`) açın.
2. Yeni bir satır ekleyerek `guid`, `Question` ve `Answer` alanlarını doldurun (tags alanını ders etiketiyle aynı bırakın).
3. Terminalde şu komutu çalıştırarak desteleri yeniden inşa edin:
```bash
./venv/bin/brain-brew run recipes/kpss.yaml
```

İnşa edilen güncel desteleri `build/` klasöründe bulabilirsiniz.

---
**KamuSinyal** - Zamanın Sinyalini Sen Belirle!
