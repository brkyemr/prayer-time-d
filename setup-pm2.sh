#!/bin/bash

# Prayer Time App PM2 Setup Script
# Bu script otomatik olarak Python interpreter ve app dizinini tespit eder

echo "🔍 Prayer Time App PM2 Kurulum Script'i başlatılıyor..."

# Mevcut kullanıcıyı tespit et
CURRENT_USER=$(whoami)
echo "👤 Mevcut kullanıcı: $CURRENT_USER"

# Mevcut dizini tespit et
CURRENT_DIR=$(pwd)
echo "📁 Mevcut dizin: $CURRENT_DIR"

# Python interpreter'ı tespit et
if [ -f "$CURRENT_DIR/venv/bin/python3" ]; then
    PYTHON_INTERPRETER="$CURRENT_DIR/venv/bin/python3"
    echo "🐍 Virtual environment Python bulundu: $PYTHON_INTERPRETER"
elif command -v python3 &> /dev/null; then
    PYTHON_INTERPRETER=$(which python3)
    echo "🐍 Sistem Python bulundu: $PYTHON_INTERPRETER"
else
    echo "❌ Python3 bulunamadı! Lütfen Python3 kurulumu yapın."
    exit 1
fi

# Environment variable'ları export et
export PYTHON_INTERPRETER="$PYTHON_INTERPRETER"
export APP_DIR="$CURRENT_DIR"

echo "🔧 Environment variables ayarlandı:"
echo "   PYTHON_INTERPRETER: $PYTHON_INTERPRETER"
echo "   APP_DIR: $APP_DIR"

# PM2 ecosystem dosyasını güncelle
echo "📝 Ecosystem config güncelleniyor..."

# Geçici config oluştur
cat > ecosystem.temp.js << EOF
module.exports = {
  apps: [{
    name: 'prayer-time-app',
    script: 'main.py',
    interpreter: '$PYTHON_INTERPRETER',
    cwd: '$APP_DIR',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: '$APP_DIR'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
EOF

# Orijinal dosyayı yedekle ve yenisini kopyala
cp ecosystem.config.js ecosystem.config.js.backup
mv ecosystem.temp.js ecosystem.config.js

echo "✅ Ecosystem config güncellendi!"
echo "📋 Yedek dosya: ecosystem.config.js.backup"

# Logs dizinini oluştur
mkdir -p logs
echo "📁 Logs dizini oluşturuldu"

# PM2 ile başlat
echo "🚀 PM2 ile uygulama başlatılıyor..."
pm2 start ecosystem.config.js

echo ""
echo "🎉 Kurulum tamamlandı!"
echo "📊 PM2 durumunu kontrol etmek için: pm2 status"
echo "📝 Logları görüntülemek için: pm2 logs prayer-time-app"
echo "🔄 Yeniden başlatmak için: pm2 restart prayer-time-app"
echo "🛑 Durdurmak için: pm2 stop prayer-time-app"
