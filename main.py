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
def home(): return "Pro Stealth Reporting Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# তোমার টোকেন ও লিঙ্ক
TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

# বিভিন্ন সোর্স এবং ব্রাউজার প্রোফাইল
REFERRERS = ["https://www.google.com/", "https://www.bing.com/", "https://www.facebook.com/", "https://t.co/"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
]

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            # ধাপ ১: আইপি ও পরিচয় নির্ধারণ
            bot.send_message(chat_id, "🔍 ধাপ ১: হাই-কোয়ালিটি আইপি ও ডিভাইস প্রোফাইল সেটআপ হচ্ছে...")
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
            driver.set_page_load_timeout(60)

            # ধাপ ২: রেফারার সেট করে লিঙ্ক ওপেন
            bot.send_message(chat_id, f"🌐 ধাপ ২: {ref} থেকে লিঙ্কে ঢোকা হচ্ছে।\n🌍 আইপি: {proxy}")
            driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": ref}})
            driver.get(DIRECT_LINK)
            
            # ধাপ ৩: স্ক্রিনশট নেওয়া
            bot.send_message(chat_id, "⏳ ধাপ ৩: পেজ লোড হয়েছে। প্রমাণের জন্য স্ক্রিনশট নেওয়া হচ্ছে...")
            time.sleep(15) 
            screenshot_path = "proof.png"
            driver.save_screenshot(screenshot_path)
            
            with open(screenshot_path, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=f"📸 সেশন: {count+1}\nডিভাইস: {agent[:20]}...\nলিঙ্ক কি সফলভাবে খুলেছে?")

            # ধাপ ৪: অ্যাক্টিভিটি সিমুলেশন
            bot.send_message(chat_id, "👀 ধাপ ৪: মানুষের মতো পেজ স্ক্রল করে ৩০ সেকেন্ড অপেক্ষা করছি...")
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(20)
            
            driver.quit()
            count += 1
            bot.send_message(chat_id, f"✅ ধাপ ৫: সেশন সফলভাবে শেষ! মোট ট্রাই: {count}")
            
            # বিরতি
            bot.send_message(chat_id, "💤 ৩ মিনিট বিরতি নেওয়া হচ্ছে...")
            time.sleep(180)
            
        except Exception as e:
            bot.send_message(chat_id, "⚠️ আইপি এরর! নতুন আইপি দিয়ে আবার চেষ্টা করছি...")
            time.sleep(15)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 প্রো-রিপোর্টিং মোড চালু হয়েছে! এখন প্রতিটি সেশনে স্ক্রিনশট পাবেন।")
        Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 কাজ বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
