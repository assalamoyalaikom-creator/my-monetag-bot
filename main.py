import os
import time
import random
import telebot
import requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Flask Server Setup for Render Health Check
app = Flask('')
@app.route('/')
def home():
    return "Monetag Secure Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# তোমার নতুন টোকেন এখানে বসানো হয়েছে
TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)

# তোমার ডিরেক্ট লিঙ্ক
DIRECT_LINK = "https://omg10.com/4/10646993" 

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            # উন্নত মানের প্রক্সি সোর্স
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA,DE&ssl=yes&anonymity=elite"
            res = requests.get(url, timeout=10)
            proxies = [p.strip() for p in res.text.strip().split('\n') if p.strip()]
            
            if not proxies:
                time.sleep(20)
                continue

            proxy = random.choice(proxies)
            
            # ব্রাউজার সেটিংস
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{proxy}')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(40)
            
            # লিঙ্ক ভিজিট করা
            driver.get(DIRECT_LINK)
            time.sleep(random.randint(20, 35)) # বাস্তবসম্মত সময় অপেক্ষা
            driver.quit()
            
            count += 1
            bot.send_message(chat_id, f"✅ নতুন বটের ভিউ সফল!\n🔢 সেশন: {count}\n🌍 IP: {proxy}")
            
            # ব্যান এড়াতে বিরতি
            time.sleep(random.randint(70, 150))
            
        except Exception as e:
            time.sleep(15)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 নতুন টোকেন দিয়ে কাজ শুরু হয়েছে! ভিউ কাউন্ট শুরু হচ্ছে...")
        Thread(target=worker, args=(message.chat.id,)).start()
    else:
        bot.reply_to(message, "বট অলরেডি চলছে!")

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    # সার্ভার চালানো
    t = Thread(target=run_flask)
    t.start()
    # টেলিগ্রাম পোলিং (Conflict এড়াতে অপশনসহ)
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
