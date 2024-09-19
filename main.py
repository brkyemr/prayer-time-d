import json
import time
import datetime
from pytz import timezone
import schedule
import pygame  # mp3 oynatmak için pygame kütüphanesi

pygame.mixer.init()
# JSON dosyasından ezan vakitlerini yükleme
with open('duisburg2024.json') as f:
    ezan_data = json.load(f)

# Zaman dilimi (CET/CEST)
local_timezone = timezone('Europe/Istanbul')  # Berlin'den İstanbul'a güncelledim

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
def selaRun(): # Sela
    print("Sela vakti! selaRun() fonksiyonu çalıştırılıyor... play sela.mp3")
    play_mp3('./sela.mp3')

# Bugünün ezan saatlerini ve gün adını JSON verisinden alacak fonksiyon
def get_today_timings():
    # Bugünün tarihini formatlıyoruz
    today = datetime.datetime.now(local_timezone).strftime("%d.%m.%Y")
    
    # Bugünün ezan vakitlerini JSON'dan buluyoruz
    for day_data in ezan_data:
        if day_data['gregorianDateShort'] == today:
            return day_data, day_data['gregorianDateLong']
    return None, None

# Her vakit için planlama fonksiyonunu yazıyoruz
def schedule_prayer_times():
    today_data, weekday = get_today_timings()  # Bugünün ezan vakitlerini ve haftanın gününü al
    if today_data:
        timings = today_data  # Tüm vakit bilgileri JSON'dan geldiği gibi
        now = datetime.datetime.now(local_timezone)
        # Her bir ezan vakti için benzer işlemleri yapacağız:
        def schedule_time(prayer_name, prayer_time, function):
            prayer_time = datetime.datetime.strptime(prayer_time, '%H:%M')
            prayer_time = prayer_time.replace(year=now.year, month=now.month, day=now.day)
            prayer_time = local_timezone.localize(prayer_time)
            schedule_time_str = prayer_time.strftime('%H:%M')
            schedule.every().day.at(schedule_time_str).do(function)
            print(f"{prayer_name} vakti {schedule_time_str} saatinde planlandı.")

        # Tüm vakitler için planlama yapıyoruz
        schedule_time('Fajr', timings['fajr'], fajrRun)
        schedule_time('Dhuhr', timings['dhuhr'], dhuhrRun)
        schedule_time('Asr', timings['asr'], asrRun)
        schedule_time('Maghrib', timings['maghrib'], maghribRun)
        schedule_time('Isha', timings['isha'], ishaRun)
        # Eğer gün Perşembe ise, Isha'dan 30 dakika önce selaRun fonksiyonunu planla
        if "Perşembe" in weekday:
            isha_time = timings['isha']
            isha_time = datetime.datetime.strptime(isha_time, '%H:%M')
            isha_time = isha_time.replace(year=now.year, month=now.month, day=now.day)
            isha_time = local_timezone.localize(isha_time)
            sela_time = isha_time - datetime.timedelta(minutes=30)  # Isha'dan 30 dakika önce
            sela_time_str = sela_time.strftime('%H:%M')
            schedule.every().day.at(sela_time_str).do(selaRun)
            print(f"Sela vakti {sela_time_str} saatinde planlandı (Perşembe).")
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