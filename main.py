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
def home(): return "Reporting Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# তোমার নতুন টোকেন
TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            # পদক্ষেপ ১: প্রক্সি খোঁজা
            bot.send_message(chat_id, "🔍 ধাপ ১: প্রক্সি সার্ভার থেকে নতুন আইপি খোঁজা হচ্ছে...")
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA&ssl=yes&anonymity=elite"
            proxies = requests.get(url).text.strip().split('\n')
            proxy = random.choice(proxies).strip()

            # পদক্ষেপ ২: আইপি কানেক্ট করা
            bot.send_message(chat_id, f"🌐 ধাপ ২: আইপি পাওয়া গেছে ({proxy})। এখন ব্রাউজার সেটআপ করা হচ্ছে...")

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{proxy}')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(35)

            # পদক্ষেপ ৩: লিঙ্ক লোড করা
            bot.send_message(chat_id, f"⏳ ধাপ ৩: মনিটেগ লিঙ্ক লোড করা হচ্ছে। দয়া করে অপেক্ষা করুন...")
            driver.get(DIRECT_LINK)
            
            # পদক্ষেপ ৪: পেজে অবস্থান করা
            bot.send_message(chat_id, "👀 ধাপ ৪: লিঙ্ক ওপেন হয়েছে। সেশন ভ্যালিড করার জন্য ৩০ সেকেন্ড অপেক্ষা করছি...")
            time.sleep(30) 
            driver.quit()
            
            # পদক্ষেপ ৫: ফলাফল জানানো
            count += 1
            bot.send_message(chat_id, f"✅ ধাপ ৫: ভিউ সফল হয়েছে! \n🔢 আজ পর্যন্ত মোট সফল ভিউ: {count}")
            
            # পরবর্তী কাজের আগে বিরতি
            bot.send_message(chat_id, "💤 এখন ২ মিনিট বিরতি নেওয়া হচ্ছে। এরপর আবার নতুন কাজ শুরু হবে।")
            time.sleep(random.randint(100, 150))
            
        except Exception as e:
            bot.send_message(chat_id, f"❌ সমস্যা হয়েছে: আইপি কানেক্ট করা যায়নি। আমি আবার চেষ্টা করছি...")
            time.sleep(10)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 রিপোর্ট মোড চালু হয়েছে! এখন আমি যা করবো সব আপনাকে মেসেজ দিয়ে জানাবো।")
        Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ সম্পূর্ণ বন্ধ করা হয়েছে। আপনার অনুমতি ছাড়া আমি আর কোনো পদক্ষেপ নেব না।")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
