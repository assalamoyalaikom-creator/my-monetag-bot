import os
import time
import random
import telebot
import requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ১. Render-এ সচল রাখার জন্য Flask সার্ভার
app = Flask('')
@app.route('/')
def home(): return "Rahim's Advanced Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. সেটিংস
TOKEN = '8654871277:AAHthU90TEdQx-58pYjaYBgDs4NOI6t9Myo'
bot = telebot.TeleBot(TOKEN)
BLOG_LINK = "https://12rahim.blogspot.com/?m=1" 

is_running = False

def get_live_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        res = requests.get(url, timeout=10)
        return res.text.strip().split('\n') if res.status_code == 200 else []
    except: return []

def start_browser_session(chat_id, count, proxy):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(40)
        driver.get(BLOG_LINK)
        
        # ১৫ সেকেন্ড অপেক্ষা ও স্ক্রল
        time.sleep(15)
        driver.execute_script("window.scrollTo(0, 500);")
        
        # ৩টি অটো-ক্লিক করার চেষ্টা (অ্যাড বা লিঙ্কে)
        for i in range(1, 4):
            try:
                # স্ক্রিনে থাকা যেকোনো লিঙ্কে ক্লিক করার চেষ্টা করবে
                elements = driver.find_elements(By.TAG_NAME, 'a')
                if elements:
                    random.choice(elements).click()
                
                bot.send_message(chat_id, f"🖱️ ক্লিক {i} সফল! (সেশন: {count})")
                time.sleep(10) # প্রতি ক্লিকের মাঝে ১০ সেকেন্ড বিরতি
            except:
                continue

        bot.send_message(chat_id, f"✅ Render সাকসেস! \n🌍 প্রক্সি: {proxy} \n🔢 সেশন: {count} শেষ।")
        return True
    except:
        return False
    finally:
        if driver: driver.quit()

def worker(chat_id):
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
        time.sleep(random.randint(20, 40))

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if is_running:
        bot.reply_to(message, "বট অলরেডি চলছে!")
        return
    is_running = True
    bot.reply_to(message, "🚀 ক্লিক অপশনসহ অটো-ট্রাফিক শুরু হয়েছে!")
    Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 বট বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
