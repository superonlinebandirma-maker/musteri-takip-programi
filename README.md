# Müşteri Takip Programı (CRM)

Profesyonel bir masaüstü müşteri yönetim sistemi.

## Özellikler

- 👥 **Müşteri Yönetimi** - Müşteri bilgileri, iletişim bilgileri, adres
- 💰 **Satış Takibi** - Satış fırsatları, sipariş takibi
- 📞 **İletişim Geçmişi** - Tüm komunikasyon kayıtları
- ✅ **Görevler & Reminders** - Görevler, hatırlatıcılar, takvim
- 📊 **Raporlama** - Satış raporları, müşteri analitiği

## Kurulum

### 1. Python Yükleme
- Python 3.9+ indirin: https://www.python.org/downloads/

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Programı Çalıştırın
```bash
python main.py
```

## Sistem Gereksinimleri
- Python 3.9+
- Windows 10+, macOS, Linux
- 500MB boş disk alanı

## İlk Kullanım
Programı açtığınızda:
1. Otomatik veritabanı oluşturulur
2. Ana menüyü göreceksiniz
3. Müşteri ekleyerek başlayabilirsiniz

## Dosya Yapısı
```
musteri-takip-programi/
├── main.py              # Ana program dosyası
├── requirements.txt     # Python kütüphaneleri
├── database.py         # Veritabanı yönetimi
├── models.py           # Veri modelleri
├── ui/                 # Arayüz modülleri
│   ├── __init__.py
│   ├── main_window.py
│   ├── customers.py
│   ├── sales.py
│   ├── communications.py
│   ├── tasks.py
│   └── reports.py
└── crm.db             # Veritabanı (otomatik oluşturulur)
```

## Sorun Giderme
- Program açılmıyorsa: Python doğru yüklenmiş mi kontrol edin
- Hata alıyorsanız: Terminal çıktısını okuyun

## Destek
Herhangi bir sorun için README dosyasını okuyun veya kodu inceleyebilirsiniz.

---
**Sürüm:** 1.0.0  
**Lisans:** MIT
