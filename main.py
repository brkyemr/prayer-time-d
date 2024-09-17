import json
import time
import datetime
from pytz import timezone
import schedule
import pygame  # mp3 oynatmak için pygame kütüphanesi

pygame.mixer.init()
# JSON dosyasından ezan vakitlerini yükleme
with open('ezan_times_2024_2030.json') as f:
    ezan_data = json.load(f)

# Zaman dilimi (CET/CEST)
local_timezone = timezone('Europe/Berlin')

def play_mp3(file):
    """mp3 dosyasını çalmak için fonksiyon"""
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def fajrRun(): # İmsak
    print("İmsak vakti! fajrRun() fonksiyonu çalıştırılıyor... play sabah.mp3")
    play_mp3('./sabah.mp3')
def dhuhrRun(): # Öğle
    print("Öğle vakti! dhuhrRun() fonksiyonu çalıştırılıyor... play ogle.mp3")
    play_mp3('./ogle.mp3')
def asrRun(): # İkindi
    print("İkindi vakti! asrRun() fonksiyonu çalıştırılıyor... play ikindi.mp3")
    play_mp3('./ikindi.mp3')
def maghribRun(): # Akşam
    print("Akşam vakti! maghribRun() fonksiyonu çalıştırılıyor... play aksam.mp3")
    play_mp3('./aksam.mp3')
def ishaRun(): # Yatsı
    print("Yatsı vakti! ishaRun() fonksiyonu çalıştırılıyor... play yatsi.mp3")
    play_mp3('./yatsi.mp3')


# Bugünün ezan saatlerini JSON verisinden alacak fonksiyon
def get_today_timings():
    # Bugünün tarihini formatlıyoruz
    today = datetime.datetime.now(local_timezone).strftime("%d-%m-%Y")
    
    # Bugünün ezan vakitlerini JSON'dan buluyoruz
    for day_data in ezan_data:
        if day_data['date']['gregorian']['date'] == today:
            return day_data['timings']
    return None

# Her vakit için planlama fonksiyonunu yazıyoruz
def schedule_prayer_times():
    timings = get_today_timings()  # Bugünün ezan vakitlerini al

    if timings:
        now = datetime.datetime.now(local_timezone)
        print("Now =>",now)
        # Her bir ezan vakti için benzer işlemleri yapacağız:
        def schedule_time(prayer_name, prayer_time, function):
            prayer_time = prayer_time.replace(' (CET)', '').replace(' (CEST)', '')
            prayer_time = datetime.datetime.strptime(prayer_time, '%H:%M')
            prayer_time = prayer_time.replace(year=now.year, month=now.month, day=now.day)
            prayer_time = local_timezone.localize(prayer_time)
            schedule_time_str = prayer_time.strftime('%H:%M')
            schedule.every().day.at(schedule_time_str).do(function)
            print(f"{prayer_name} vakti {schedule_time_str} saatinde planlandı.")

        # Tüm vakitler için planlama yapıyoruz
        schedule_time('Fajr', timings['Fajr'], fajrRun)
        schedule_time('Dhuhr', timings['Dhuhr'], dhuhrRun)
        schedule_time('Asr', timings['Asr'], asrRun)
        schedule_time('Maghrib', timings['Maghrib'], maghribRun)
        schedule_time('Isha', timings['Isha'], ishaRun)

# Yeni gün geldiğinde planlamaları sıfırlayan fonksiyon
def clear_schedule_for_new_day():
    schedule.clear()
    schedule_prayer_times()

# Ana döngü: sürekli programı kontrol eder
def run_scheduler():
    last_day = None
    
    while True:
        today = datetime.datetime.now(local_timezone).day
        if today != last_day:  # Eğer gün değiştiyse
            clear_schedule_for_new_day()  # Yeni gün için planlamayı sıfırla
            last_day = today  # Yeni günü kaydet
        
        schedule.run_pending()  # Planlanmış işleri çalıştır
        time.sleep(60)  # 60 saniye bekleyip tekrar kontrol et

if __name__ == "__main__":
    run_scheduler()


 #test için 17-09-2024 tarihi manupule edildi