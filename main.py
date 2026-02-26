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
def home(): return "OwlProxy Premium Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

# তোমার দেওয়া সবগুলো আইপি সঠিক ফরম্যাটে সাজানো হয়েছে
PROXY_LIST = [
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_08973779_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_22370385_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_07614033_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_23694578_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_81740427_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_53605477_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_03703681_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_44841077_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_32179308_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_48513029_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_IT_st__city_sid_63951439_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_66490565_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_36437645_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_45434708_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_05849572_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_10521676_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_36865015_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_99439321_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_45438572_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_54651619_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_78318355_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_BR_st__city_sid_05108010_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_CA_st__city_sid_06046386_time_5:2325276@change4.owlproxy.com:7778",
    "socks5://G67RxG84ts40_custom_zone_US_st__city_sid_52194465_time_5:2325276@change4.owlproxy.com:7778"
]

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            bot.send_message(chat_id, "🔍 ধাপ ১: লিস্ট থেকে আইপি চেক করা হচ্ছে...")
            proxy = random.choice(PROXY_LIST)
            
            # আইপি ইনফো বের করা (মেসেজের জন্য)
            ip_info = proxy.split('_zone_')[1].split('_st_')[0] if '_zone_' in proxy else "Unknown"

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument(f'--proxy-server={proxy}')
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(60)

            bot.send_message(chat_id, f"🌐 আইপি কানেক্টেড: {ip_info}\n⏳ লিঙ্ক লোড হচ্ছে...")
            driver.get(DIRECT_LINK)
            
            time.sleep(30) # পেজ লোড ও অবস্থানের জন্য সময়

            # স্ক্রিনশট নেওয়া
            screenshot = "premium_proof.png"
            driver.save_screenshot(screenshot)
            with open(screenshot, "rb") as photo:
                bot.send_photo(chat_id, photo, caption=f"📸 সেশন: {count+1}\n🌍 কান্ট্রি: {ip_info}\n\nসফলভাবে পেজ লোড হয়েছে!")

            driver.quit()
            count += 1
            bot.send_message(chat_id, f"✅ কাজ শেষ! মোট সফল ভিউ: {count}")
            
            time.sleep(180) # ৩ মিনিট বিরতি

        except Exception as e:
            bot.send_message(chat_id, "❌ এই আইপিটি লোড নিতে পারেনি। অন্যটি চেষ্টা করছি...")
            time.sleep(10)

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    is_running = True
    bot.reply_to(message, "🚀 প্রিমিয়াম আইপি দিয়ে কাজ শুরু! প্রতিটি সেশনে স্ক্রিনশট পাবেন।")
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
