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
def home(): return "Reporting & Security Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
]

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            # ধাপ ১: প্রক্সি ও ডিভাইস সেটআপ
            bot.send_message(chat_id, "🔍 ধাপ ১: নতুন একটি হাই-কোয়ালিটি আইপি (Proxy) খোঁজা হচ্ছে...")
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA,DE,FR&ssl=yes&anonymity=elite"
            proxies = requests.get(url).text.strip().split('\n')
            proxy = random.choice(proxies).strip()
            
            agent = random.choice(USER_AGENTS)
            bot.send_message(chat_id, f"🌐 ধাপ ২: আইপি পাওয়া গেছে ({proxy})। এখন ব্রাউজারকে {agent[:20]}... ডিভাইসে রূপান্তর করছি।")

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{proxy}')
            options.add_argument(f'user-agent={agent}')
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(45)

            # ধাপ ৩: মনিটেগ লিঙ্ক লোড
            bot.send_message(chat_id, "⏳ ধাপ ৩: মনিটেগ লিঙ্ক লোড করা হচ্ছে। দয়া করে অপেক্ষা করুন...")
            driver.get(DIRECT_LINK)
            
            # ধাপ ৪: সেশন ভ্যালিডেশন (মানুষের মতো আচরণ)
            bot.send_message(chat_id, "👀 ধাপ ৪: লিঙ্ক সফলভাবে ওপেন হয়েছে। সেশনটি আসল মানুষের মতো করতে স্ক্রল করা হচ্ছে এবং ৪০ সেকেন্ড অপেক্ষা করছি...")
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(20)
            driver.execute_script("window.scrollTo(400, 0);")
            time.sleep(10)
            
            driver.quit()
            
            # ধাপ ৫: ফলাফল
            count += 1
            bot.send_message(chat_id, f"✅ ধাপ ৫: কাজ সম্পন্ন! \n🔢 সেশন নম্বর: {count} \n⚠️ দ্রষ্টব্য: মনিটেগ ড্যাশবোর্ডে আপডেট হতে কিছুটা সময় নিতে পারে।")
            
            # পরবর্তী কাজের আগে বিরতি
            bot.send_message(chat_id, "💤 এখন আমি ৩ মিনিট বিশ্রাম নেব, যাতে মনিটেগ সন্দেহ না করে। এরপর আবার আপনাকে জানিয়ে নতুন কাজ শুরু করব।")
            time.sleep(180)
            
        except Exception as e:
            bot.send_message(chat_id, "❌ এই আইপিটি কাজ করছে না। আমি আবার নতুন আইপি দিয়ে চেষ্টা করছি...")
            time.sleep(10)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 রিপোর্ট মোড চালু হয়েছে! এখন থেকে আমার প্রতিটি পদক্ষেপ আপনাকে মেসেজ দিয়ে জানাবো।")
        Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ বন্ধ করা হয়েছে। আপনার অনুমতি ছাড়া আমি আর কিছুই করবো না।")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
