# 🕌 Prayer Time App - Ezan Vakti Uygulaması

Bu uygulama, belirlenen ezan vakitlerinde otomatik olarak ses çalan bir Python uygulamasıdır. Raspberry Pi üzerinde PM2 ile çalışacak şekilde tasarlanmıştır.

## 📋 Özellikler

- 🕐 Otomatik ezan vakti tespiti
- 🔊 MP3 ses dosyaları ile ezan çalma
- 📅 JSON dosyasından güncel ezan vakitleri
- 🔄 PM2 ile sürekli çalışma
- 🚀 Sistem başlangıcında otomatik başlatma
- 📝 Detaylı loglama

## 🛠️ Gereksinimler

- Raspberry Pi (Raspberry Pi OS)
- Python 3.7+
- Node.js 16+
- PM2
- Ses çıkışı (3.5mm jack veya HDMI)

## 📦 Kurulum Adımları

### 1. Sistem Güncellemeleri
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Python ve Gerekli Paketlerin Kurulumu
```bash
# Python3 ve pip kurulumu
sudo apt install python3 python3-pip python3-venv -y

# Ses sistemi için gerekli paketler
sudo apt install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y

# SDL ve pygame için gerekli paketler
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev -y
```

### 3. Node.js ve PM2 Kurulumu
```bash
# Node.js kurulumu
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs -y

# PM2 global kurulumu
sudo npm install -g pm2
```

### 4. Proje Kurulumu
```bash
# Proje dizinine git
cd /home/ezan/Desktop/prayer-time-d

# Python virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Gerekli Python paketlerini kur
pip install -r requirements.txt

# pygame için ek kurulum (Raspberry Pi için)
pip install pygame --pre
```

### 5. Ses Sistemi Konfigürasyonu
```bash
# Ses kartını kontrol et
aplay -l

# HDMI ses çıkışı için (opsiyonel)
sudo raspi-config
# System Options > Audio > HDMI

# Veya analog ses çıkışı için
sudo raspi-config
# System Options > Audio > 3.5mm jack
```

## 🚀 PM2 ile Çalıştırma

### Otomatik Kurulum (Önerilen)
```bash
# Setup script'ini çalıştırılabilir yap
chmod +x setup-pm2.sh

# Setup script'ini çalıştır
./setup-pm2.sh
```

### Manuel Kurulum
```bash
# Environment variable'ları ayarla (kendi kullanıcı adınızla değiştirin)
export PYTHON_INTERPRETER="/home/kullanici_adi/prayer-time-d/venv/bin/python3"
export APP_DIR="/home/kullanici_adi/prayer-time-d"

# PM2 ile başlat
pm2 start ecosystem.config.js
```

## 📊 PM2 Komutları

```bash
# Uygulama durumunu kontrol et
pm2 status

# Logları görüntüle
pm2 logs prayer-time-app

# Uygulamayı yeniden başlat
pm2 restart prayer-time-app

# Uygulamayı durdur
pm2 stop prayer-time-app

# Uygulamayı sil
pm2 delete prayer-time-app

# PM2 monitörünü aç
pm2 monit
```

## 🔄 Sistem Başlangıcında Otomatik Başlatma

```bash
# PM2 startup script'ini oluştur
pm2 startup

# Mevcut PM2 konfigürasyonunu kaydet
pm2 save
```

## 📁 Dosya Yapısı

```
prayer-time-d/
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Python bağımlılıkları
├── ecosystem.config.js     # PM2 konfigürasyonu
├── setup-pm2.sh           # Otomatik kurulum script'i
├── README.md              # Bu dosya
├── logs/                  # Log dosyaları (otomatik oluşturulur)
├── venv/                  # Python virtual environment
├── *.mp3                  # Ezan ses dosyaları
└── *.json                 # Ezan vakti verileri
```

## ⚙️ Konfigürasyon

### Zaman Dilimi Değiştirme
`main.py` dosyasında şu satırı bulun ve değiştirin:
```python
local_timezone = timezone('Europe/Istanbul')  # Kendi zaman diliminizi yazın
```

### Ezan Vakti Dosyası Değiştirme
`main.py` dosyasında şu satırı bulun ve değiştirin:
```python
with open('duisburg2025.json') as f:  # Kendi JSON dosyanızı yazın
```

## 🐛 Hata Ayıklama

### Ses Sorunları
```bash
# Ses testi
aplay -D hw:0,0 test.mp3

# Ses sistemi logları
dmesg | grep -i audio
```

### Python Sorunları
```bash
# Python testi
python3 -c "import pygame; print('Pygame kurulumu başarılı')"

# Virtual environment testi
source venv/bin/activate
python3 main.py
```

### PM2 Sorunları
```bash
# PM2 loglarını takip et
pm2 logs prayer-time-app --lines 100

# Sistem loglarını kontrol et
sudo journalctl -u pm2-pi -f
```

## 📝 Log Dosyaları

Uygulama çalışırken aşağıdaki log dosyaları oluşturulur:
- `logs/out.log` - Standart çıktı logları
- `logs/err.log` - Hata logları
- `logs/combined.log` - Birleşik loglar

## 🔧 Bakım

### Güncellemeler
```bash
# Sistem güncellemeleri
sudo apt update && sudo apt upgrade -y

# Python paketlerini güncelle
source venv/bin/activate
pip install --upgrade -r requirements.txt

# PM2'yi güncelle
sudo npm update -g pm2
```

### Yedekleme
```bash
# Proje dizinini yedekle
tar -czf prayer-time-backup-$(date +%Y%m%d).tar.gz /home/ezan/Desktop/prayer-time-d

# PM2 konfigürasyonunu yedekle
pm2 save
```

## 🆘 Sorun Giderme

### Uygulama Başlamıyor
1. PM2 durumunu kontrol edin: `pm2 status`
2. Logları inceleyin: `pm2 logs prayer-time-app`
3. Python interpreter yolunu kontrol edin
4. Virtual environment'ın aktif olduğundan emin olun

### Ses Çıkmıyor
1. Ses seviyesini kontrol edin: `alsamixer`
2. Ses çıkış ayarını kontrol edin: `aplay -l`
3. HDMI/3.5mm jack ayarını kontrol edin
4. MP3 dosyalarının mevcut olduğundan emin olun

### Ezan Vakitleri Yanlış
1. JSON dosyasının güncel olduğundan emin olun
2. Zaman dilimi ayarını kontrol edin
3. Sistem saatini kontrol edin: `date`

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. README dosyasını tekrar okuyun
2. Log dosyalarını kontrol edin
3. GitHub Issues'da sorun bildirin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---
