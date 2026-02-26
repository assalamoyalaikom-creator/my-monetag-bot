import os
import zipfile
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
def home(): return "All Proxy Traffic Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
BLOG_LINK = "https://12rahim.blogspot.com/" 

# তোমার দেওয়া ৩৩টি আইপি এখানে লিস্ট করা হলো
PROXY_LIST = [
    # US Proxies
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_52194465_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_89578005_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_16407407_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_17563035_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_06397473_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_85008078_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_58357529_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_81151560_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_34417649_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_89583721_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_25603640_time_5:2325276",
    
    # CA Proxies
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_06046386_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_42951752_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_86689601_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_82237273_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_82171049_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_84123886_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_52437232_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_96837185_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_66860789_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_79322369_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_97263534_time_5:2325276",
    
    # BR Proxies
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_66490565_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_36437645_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_45434708_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_05849572_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_10521676_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_36865015_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_99439321_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_45438572_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_54651619_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_78318355_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_05108010_time_5:2325276",
    
    # IT Proxies
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_08973779_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_22370385_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_07614033_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_23694578_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_81740427_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_53605477_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_03703681_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_44841077_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_32179308_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_48513029_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_63951439_time_5:2325276"
]

def create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
    
    extension = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return extension

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            proxy_raw = random.choice(PROXY_LIST)
            host, port, user, password = proxy_raw.split(':')
            country = user.split('_zone_')[1][:2] if '_zone_' in user else "??"

            bot.send_message(chat_id, f"🛡️ সেশন {count+1}: {country} আইপি দিয়ে চেক শুরু হচ্ছে...")

            # ভালো আইপি চেক করা (Requests দিয়ে)
            try:
                test_proxies = {"http": f"http://{user}:{password}@{host}:{port}", "https": f"http://{user}:{password}@{host}:{port}"}
                requests.get("https://www.google.com", proxies=test_proxies, timeout=12)
            except:
                bot.send_message(chat_id, f"❌ {country} আইপি ডাউন। অন্যটি ট্রাই করছি...")
                continue

            plugin_file = create_proxy_auth_extension(host, port, user, password)
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_extension(plugin_file)

            driver = webdriver.Chrome(options=options)
            
            bot.send_message(chat_id, f"📡 ব্লগে ঢুকেছি। ২০ সেকেন্ড অপেক্ষা করছি...")
            driver.get(BLOG_LINK)
            
            # ২০ সেকেন্ড ওয়েট
            time.sleep(20) 
            
            current_url = driver.current_url
            screenshot = "final_check.png"
            driver.save_screenshot(screenshot)
            
            with open(screenshot, "rb") as f:
                bot.send_photo(chat_id, f, caption=f"📸 সেশন: {count+1}\n🌍 কান্ট্রি: {country}\n⏱️ ২০ সেকেন্ড পর স্ক্রিনশট নেওয়া হয়েছে।")

            driver.quit()
            count += 1
            time.sleep(180) 
            
        except Exception as e:
            time.sleep(10)

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    is_running = True
    bot.reply_to(message, "🚀 সব আইপি এবং ২০ সেকেন্ড ডিলে মোড চালু!")
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
