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
def home(): return "Proxy-Verified Stealth Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

REFERRERS = ["https://www.google.com/", "https://www.bing.com/", "https://www.facebook.com/"]
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
            bot.send_message(chat_id, "🔍 ধাপ ১: প্রক্সি সার্ভার থেকে কাজ করছে এমন আইপি খোঁজা হচ্ছে...")
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=US,GB,CA&ssl=yes&anonymity=elite"
            proxies = requests.get(url).text.strip().split('\n')
            
            valid_proxy = None
            # ৫ বার চেষ্টা করবে একটি সচল আইপি খুঁজে পেতে
            for _ in range(5):
                p = random.choice(proxies).strip()
                try:
                    # গুগলে রিকোয়েস্ট পাঠিয়ে আইপি চেক করা হচ্ছে
                    response = requests.get("https://www.google.com", proxies={"http": f"http://{p}", "https": f"http://{p}"}, timeout=5)
                    if response.status_code == 200:
                        valid_proxy = p
                        break
                except:
                    continue
            
            if not valid_proxy:
                bot.send_message(chat_id, "❌ কোনো সচল আইপি পাওয়া যায়নি। ১০ সেকেন্ড পর আবার চেষ্টা করছি...")
                time.sleep(10)
                continue

            ref = random.choice(REFERRERS)
            agent = random.choice(USER_AGENTS)

            bot.send_message(chat_id, f"✅ সচল আইপি পাওয়া গেছে!\n🌐 আইপি: {valid_proxy}\n🔗 সোর্স: {ref}")

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--proxy-server=http://{valid_proxy}')
            options.add_argument(f'user-agent={agent}')
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(60)

            bot.send_message(chat_id, "⏳ ধাপ ২: মনিটেগ লিঙ্ক লোড করা হচ্ছে। একটু অপেক্ষা করুন...")
            driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": ref}})
            driver.get(DIRECT_LINK)
            
            # পেজ লোড হওয়ার জন্য সময় দেওয়া
            time.sleep(20) 
            
            # প্রমাণের জন্য স্ক্রিনশট নেওয়া
            bot.send_message(chat_id, "📸 ধাপ ৩: পেজটি কি সফলভাবে লোড হয়েছে? স্ক্রিনশট দেখুন:")
            screenshot_path = "live_proof.png"
            driver.save_screenshot(screenshot_path)
            
            with open(screenshot_path, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=f"🚀 সেশন: {count+1}\n🌐 ব্যবহৃত আইপি: {valid_proxy}\n\nসাদা পেজ বা এরর আসলে আইপিটি কাজ করেনি।")

            # অ্যাক্টিভিটি সিমুলেশন
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(15)
            
            driver.quit()
            count += 1
            bot.send_message(chat_id, f"✅ ধাপ ৪: সেশন শেষ! মোট সফল ট্রাই: {count}")
            
            time.sleep(random.randint(120, 200))
            
        except Exception as e:
            time.sleep(10)
            continue

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 প্রক্সি ভেরিফাইড মোড চালু হয়েছে! এখন প্রতিটি কাজে স্ক্রিনশট পাবেন।")
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
