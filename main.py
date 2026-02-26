import os
import zipfile
import time
import random
import telebot
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask('')
@app.route('/')
def home(): return "Proxy Auth Patch is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
DIRECT_LINK = "https://omg10.com/4/10646993" 

# তোমার দেওয়া সবগুলো আইপি এখানে লিস্ট করা হয়েছে
PROXY_LIST = [
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_66490565_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_36437645_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_45434708_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_05849572_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BR_st__city_sid_10521676_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_06046386_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_42951752_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_86689601_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_52194465_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_89578005_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_16407407_time_5:2325276"
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
            
            bot.send_message(chat_id, f"🛡️ অথেন্টিকেশন প্যাচ ব্যবহার করা হচ্ছে...\n🌍 আইপি কান্ট্রি: {user.split('_zone_')[1][:2]}")

            plugin_file = create_proxy_auth_extension(host, port, user, password)
            
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_extension(plugin_file)

            driver = webdriver.Chrome(options=options)
            driver.get(DIRECT_LINK)
            
            time.sleep(30) # লোড হওয়ার সময়
            
            screenshot = "auth_proof.png"
            driver.save_screenshot(screenshot)
            with open(screenshot, "rb") as f:
                bot.send_photo(chat_id, f, caption=f"📸 সেশন: {count+1}\n✅ যদি এবারও এরর আসে, তবে বুঝতে হবে ক্লাউড সার্ভার থেকে এই আইপিগুলো ব্লকড।")

            driver.quit()
            count += 1
            time.sleep(150)
        except Exception as e:
            time.sleep(10)

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    is_running = True
    bot.reply_to(message, "🚀 প্রক্সি অথেন্টিকেশন প্যাচ ও সম্পূর্ণ লিস্ট নিয়ে কাজ শুরু!")
    Thread(target=worker, args=(message.chat.id,)).start()

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
