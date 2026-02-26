import os
import time
import random
import telebot
import requests
import json
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ১. Render-এ সচল রাখার জন্য Flask সার্ভার
app = Flask('')
@app.route('/')
def home(): return "Rahim's Render Bot is Active!"

def run():
    # Render নিজে থেকে PORT সেট করে দেয়, তাই এটি জরুরি
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. তোমার টেলিগ্রাম টোকেন ও ব্লগ লিঙ্ক
TOKEN = '8654871277:AAHthU90TEdQx-58pYjaYBgDs4NOI6t9Myo'
bot = telebot.TeleBot(TOKEN)
BLOG_LINK = "https://12rahim.blogspot.com/?m=1" 

is_running = False

def get_live_proxies():
    """ইন্টারনেট থেকে লাইভ প্রক্সি সংগ্রহ"""
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=us,uk,ca,it&ssl=all&anonymity=all"
        res = requests.get(url, timeout=10)
        return res.text.strip().split('\n') if res.status_code == 200 else []
    except: return []

def start_browser_session(chat_id, count, proxy):
    """ব্রাউজার দিয়ে ব্লগ ভিজিট করা"""
    options = Options()
    options.add_argument('--headless=new') # ব্যাকগ্রাউন্ডে চলবে
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={ua}')

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(35)
        
        # ব্লগে প্রবেশ
        driver.get(BLOG_LINK)
        
        # ১৫-২৫ সেকেন্ড অপেক্ষা (ভিউ কাউন্ট হওয়ার জন্য)
        wait_time = random.randint(15, 25)
        time.sleep(wait_time)
        
        bot.send_message(chat_id, f"✅ Render সাকসেস! \n🌍 প্রক্সি: {proxy} \n⌛ সময়: {wait_time}s \n🔢 সেশন: {count}")
        return True
    except:
        return False
    finally:
        if driver: driver.quit()

def worker(chat_id):
    """বটের কাজের মূল লুপ"""
    global is_running
    count = 0
    while is_running:
        proxies = get_live_proxies()
        if not proxies:
            time.sleep(20)
            continue
        
        count += 1
        proxy = random.choice(proxies).strip()
        start_browser_session(chat_id, count, proxy)
        
        # সেশনগুলোর মাঝে বিরতি (নিরাপত্তার জন্য)
        time.sleep(random.randint(30, 60))

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if is_running:
        bot.reply_to(message, "বট অলরেডি চলছে!")
        return
    is_running = True
    bot.reply_to(message, "🚀 Render-এ অটো-ট্রাফিক শুরু হয়েছে!")
    Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 বট বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    # Flask সার্ভার চালু করা
    t = Thread(target=run)
    t.start()
    # টেলিগ্রাম বট চালু করা
    bot.infinity_polling()
