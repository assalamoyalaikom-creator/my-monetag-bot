import os
import time
import random
import telebot
import requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask('')
@app.route('/')
def home(): return "Rahim's New Fresh Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# এখানে তোমার একদম নতুন টোকেনটি বসাও
TOKEN = 'এখানে_নতুন_টোকেন_বসাও' 
bot = telebot.TeleBot(TOKEN)

# তোমার ডিরেক্ট লিঙ্ক
DIRECT_LINK = "https://omg10.com/4/10646993" 

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S24 Ultra) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36"
]

is_running = False

def get_high_quality_proxies():
    try:
        # শুধু টপ দেশের আইপি ফিল্টার
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=4000&country=US,GB,CA,DE&ssl=yes&anonymity=elite"
        res = requests.get(url, timeout=10)
        return [p.strip() for p in res.text.strip().split('\n') if p.strip()] if res.status_code == 200 else []
    except: return []

def is_proxy_live(proxy):
    try:
        response = requests.get("https://www.google.com", proxies={"http": f"http://{proxy}"}, timeout=3)
        return response.status_code == 200
    except: return False

def start_secure_session(chat_id, count, proxy):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(45)
        driver.get(DIRECT_LINK)
        
        # ১৫-৩০ সেকেন্ড র্যান্ডম অপেক্ষা
        time.sleep(random.randint(15, 30)) 
        
        bot.send_message(chat_id, f"✅ নতুন বটের প্রথম ভিউ সফল! \n🌍 আইপি: {proxy} \n🔢 সেশন: {count}")
        return True
    except: return False
    finally:
        if driver: driver.quit()

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        proxies = get_high_quality_proxies()
        if not proxies:
            time.sleep(20)
            continue
        
        proxy = random.choice(proxies)
        if is_proxy_live(proxy):
            count += 1
            start_secure_session(chat_id, count, proxy)
            # বড় বিরতি যাতে কোনোভাবেই ব্যান না হও
            time.sleep(random.randint(70, 160)) 
        else: continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if is_running:
        bot.reply_to(message, "বট অলরেডি চলছে!")
        return
    is_running = True
    bot.reply_to(message, "🌟 নতুন টোকেন দিয়ে কাজ শুরু হয়েছে! আইপি ফিল্টার করা হচ্ছে...")
    Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 বট বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    # Conflict এড়াতে polling অপশনটি আরও নিরাপদ করা হয়েছে
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
