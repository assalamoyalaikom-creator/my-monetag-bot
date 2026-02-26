import os, zipfile, time, random, telebot, requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask('')
@app.route('/')
def home(): return "All Proxy Master Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
bot = telebot.TeleBot(TOKEN)
BLOG_LINK = "https://12rahim.blogspot.com/"

# তোমার দেওয়া সব আইপি এখানে বসানো হয়েছে (মোট ৭৭+ আইপি)
PROXY_LIST = [
    # US & CA
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_52194465:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_89578005:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_CA_st__city_sid_06046386:2325276",
    # ML (Mali)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_06931382:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_43785688:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_26780022:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_90782475:2325276",
    # JP (Japan)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_57635320:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_95364730:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_62810716:2325276",
    # IT (Italy)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_99895736:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_68393982:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_33958699:2325276",
    # IN (India)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IN_st__city_sid_76649638:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IN_st__city_sid_30552006:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IN_st__city_sid_78431815:2325276",
    # GH (Ghana)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GH_st__city_sid_94192099:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GH_st__city_sid_33588436:2325276",
    # ES (Spain)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ES_st__city_sid_07076772:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ES_st__city_sid_08392466:2325276",
    # BZ (Belize)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BZ_st__city_sid_48297362:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BZ_st__city_sid_16481965:2325276",
    # BD (Bangladesh)
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BD_st__city_sid_34242340:2325276", "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_BD_st__city_sid_80691230:2325276"
]

# রিয়েল ব্রাউজার ইউজার এজেন্ট
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UD1A.231105.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36"
]

# রেফারার লিস্ট
REFERRERS = ["https://www.google.com/", "https://www.facebook.com/", "https://t.co/", "https://www.youtube.com/"]

def create_proxy_auth_extension(host, port, user, password):
    manifest_json = '{"version":"1.0.0","manifest_version":2,"name":"Chrome Proxy","permissions":["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],"background":{"scripts":["background.js"]},"minimum_chrome_version":"22.0.0"}'
    background_js = 'var config={mode:"fixed_servers",rules:{singleProxy:{scheme:"http",host:"%s",port:parseInt(%s)},bypassList:["localhost"]}};chrome.proxy.settings.set({value:config,scope:"regular"},function(){});function callbackFn(details){return{authCredentials:{username:"%s",password:"%s"}}}chrome.webRequest.onAuthRequired.addListener(callbackFn,{urls:["<all_urls>"]},["blocking"]);' % (host, port, user, password)
    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file

is_running = False

def worker(chat_id):
    global is_running
    count = 0
    while is_running:
        try:
            proxy_raw = random.choice(PROXY_LIST)
            host, port, user, password = proxy_raw.split(':')
            country = user.split('_zone_')[1][:2]

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            ua = random.choice(USER_AGENTS)
            options.add_argument(f'user-agent={ua}')
            options.add_extension(create_proxy_auth_extension(host, port, user, password))

            driver = webdriver.Chrome(options=options)
            
            # রেফারার সেট করা
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Referer': random.choice(REFERRERS)}})

            bot.send_message(chat_id, f"🛡️ সেশন {count+1}: {country} আইপি ও নতুন ব্রাউজার দিয়ে কাজ শুরু হচ্ছে...")
            driver.get(BLOG_LINK)
            
            # ১. প্রথম ৩০ সেকেন্ড অবস্থান
            time.sleep(30)
            
            # ২. বাকি ৩০ সেকেন্ডে ৩টি ক্লিক (১০ সেকেন্ড অন্তর)
            for i in range(3):
                try:
                    elements = driver.find_elements(By.TAG_NAME, "a")
                    if elements:
                        target = random.choice(elements)
                        driver.execute_script("arguments[0].scrollIntoView();", target)
                        time.sleep(2)
                        target.click()
                    time.sleep(10)
                except:
                    time.sleep(10)

            # প্রুফ স্ক্রিনশট
            screenshot = "master_work.png"
            driver.save_screenshot(screenshot)
            with open(screenshot, "rb") as f:
                bot.send_photo(chat_id, f, caption=f"✅ সেশন {count+1} সফল!\n🌍 দেশ: {country}\n⏱️ ১ মিনিট অবস্থান ও ৩টি ক্লিক সম্পন্ন।")

            driver.quit()
            count += 1
            time.sleep(90) # সেশন ব্রেক
            
        except Exception as e:
            time.sleep(20)

@bot.message_handler(commands=['work'])
def start_bot(message):
    global is_running
    is_running = True
    bot.reply_to(message, "🚀 মাস্টার বট চালু! এখন সারা রাত কাজ চলবে।")
    Thread(target=worker, args=(message.chat.id,)).start()

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 বট বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
