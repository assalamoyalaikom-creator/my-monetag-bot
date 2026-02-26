import os
import time
import random
import telebot
import requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Flask Server Setup
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running Securely!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# তোমার নতুন বট টোকেন এখানে বসাও
TOKEN = 'এখানে_নতুন_টোকেন_বসাও'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993"

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            # প্রক্সি ফিল্টারিং
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA&ssl=yes&anonymity=elite"
            proxies = requests.get(url).text.strip().split('\n')
            proxy = random.choice(proxies).strip()

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{proxy}')
            
            driver = webdriver.Chrome(options=options)
            driver.get(DIRECT_LINK)
            time.sleep(25)
            driver.quit()
            
            count += 1
            bot.send_message(chat_id, f"✅ ভিউ সফল! সেশন: {count} \n🌍 IP: {proxy}")
            time.sleep(random.randint(60, 120))
        except:
            time.sleep(10)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 কাজ শুরু হয়েছে!")
        Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    # Flask সার্ভার আলাদা থ্রেডে চালানো
    t = Thread(target=run_flask)
    t.start()
    # টেলিগ্রাম পোলিং শুরু
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
