import os

def soru_isaretlerini_duzelt(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print(f"❌ Hata: '{dosya_yolu}' dosyası bulunamadı.")
        return

    print(f"🔄 '{dosya_yolu}' dosyası okunuyor...")
    
    # Dosya kodlamasını tespit et
    kodlamalar = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1254']
    okundu = False
    satirlar = []
    kullanilan_kodlama = None
    
    for kodlama in kodlamalar:
        try:
            with open(dosya_yolu, 'r', encoding=kodlama) as f:
                satirlar = f.readlines()
            kullanilan_kodlama = kodlama
            okundu = True
            break
        except (UnicodeDecodeError, LookupError):
            continue
            
    if not okundu:
        print("❌ Hata: Dosya kodlaması çözümlenemedi.")
        return

    yeni_satirlar = []
    duzeltilen_sayisi = 0
    
    print("\n✍️ Düzeltmeler yapılıyor:")
    print("=" * 70)
    
    for satir_no, satir in enumerate(satirlar, 1):
        q_count = satir.count('?')
        if q_count > 1:
            duzeltilen_sayisi += 1
            
            # İlk soru işaretini (soru ayracını) bul
            ilk_idx = satir.find('?')
            soru_kismi = satir[:ilk_idx + 1]
            cevap_kismi = satir[ilk_idx + 1:]
            
            # Cevap kısmındaki ekstra soru işaretlerini düzeltelim
            
            # 1. Görsel linklerinden önceki ". ? (Image..." veya similar durumları temizle
            cevap_kismi = cevap_kismi.replace('. ?', '.')
            cevap_kismi = cevap_kismi.replace('? (Image', '(Image')
            
            # 2. Geriye kalan tüm soru işaretlerini '.' ile değiştir
            cevap_kismi = cevap_kismi.replace('?', '.')
            
            yeni_satir = soru_kismi + cevap_kismi
            yeni_satirlar.append(yeni_satir)
            
            print(f"📍 Satır {satir_no}:")
            print(f"   [Eski]: {satir.strip()}")
            print(f"   [Yeni]: {yeni_satir.strip()}")
            print("-" * 70)
        else:
            yeni_satirlar.append(satir)
            
    if duzeltilen_sayisi > 0:
        # Değişiklikleri dosyaya geri yaz
        try:
            with open(dosya_yolu, 'w', encoding=kullanilan_kodlama) as f:
                f.writelines(yeni_satirlar)
            print(f"✅ Başarılı: Toplam {duzeltilen_sayisi} satır düzeltildi ve '{dosya_yolu}' dosyasına kaydedildi!")
        except Exception as e:
            print(f"❌ Dosya yazılırken bir hata oluştu: {e}")
    else:
        print("ℹ️ Dosyada birden fazla soru işareti içeren satır bulunamadı, herhangi bir değişiklik yapılmadı.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dosya = sys.argv[1]
    else:
        dosya = "src/raw_data/cografya.txt"
        
    soru_isaretlerini_duzelt(dosya)
