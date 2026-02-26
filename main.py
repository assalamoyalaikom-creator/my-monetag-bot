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
def home(): return "Final Stealth Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

# রেফারার লিস্ট (কোথা থেকে ভিজিটর আসছে দেখাবে)
REFERRERS = ["https://www.google.com/", "https://www.youtube.com/", "https://www.bing.com/", "https://twitter.com/"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
]

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            bot.send_message(chat_id, "🔍 ধাপ ১: প্রক্সি এবং ট্রাফিক সোর্স সেটআপ হচ্ছে...")
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA,DE,FR&ssl=yes&anonymity=elite"
            proxies = requests.get(url).text.strip().split('\n')
            proxy = random.choice(proxies).strip()
            
            ref = random.choice(REFERRERS)
            agent = random.choice(USER_AGENTS)

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{proxy}')
            options.add_argument(f'user-agent={agent}')
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)
            
            # রেফারার মাস্কিং (গুগল থেকে আসছে এমন দেখানো)
            driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                "headers": {"Referer": ref}
            })

            bot.send_message(chat_id, f"🌐 ধাপ ২: {ref} থেকে লিঙ্কে ঢোকা হচ্ছে। আইপি: {proxy}")
            driver.get(DIRECT_LINK)
            
            bot.send_message(chat_id, "⏳ ধাপ ৩: পেজ স্ক্রল এবং অ্যাক্টিভিটি সিমুলেট করা হচ্ছে...")
            time.sleep(15)
            driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(20)
            
            driver.quit()
            count += 1
            bot.send_message(chat_id, f"✅ ধাপ ৪: সেশন সফল! মোট ট্রাই: {count}")
            
            # বড় গ্যাপ দেওয়া হচ্ছে যাতে সন্দেহ না হয়
            time.sleep(random.randint(150, 250))
            
        except Exception as e:
            time.sleep(15)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 স্টিলথ মোড চালু! এখন মনিটেগ ভাববে ভিজিটর গুগল/ইউটিউব থেকে আসছে।")
        Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ বন্ধ।")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
