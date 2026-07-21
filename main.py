import os
import time
import requests
from flask import Flask
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    try:
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text}, timeout=10)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def background_stock_check():
    # Selenium işlemini arka planda (kilitlenmeden) yürüten fonksiyon
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(URL)
        time.sleep(4)
        
        stok_listesi = driver.execute_script("return PRODUCT_DETAIL_SIZE_DATA;")
        
        if stok_listesi:
            hedef_bedenler = ["34", "36","38"]
            stoka_girenler = []
            
            for beden_bilgisi in stok_listesi:
                beden = beden_bilgisi.get("Size")
                stok_miktari = beden_bilgisi.get("StockQuantity", 0)
                
                if beden in hedef_bedenler and stok_miktari > 0:
                    stoka_girenler.append(f"{beden} Beden (Kalan: {stok_miktari})")
            
            if stoka_girenler:
                bulunanlar_str = ", ".join(stoka_girenler)
                send_telegram_message(f"🚨 MÜJDE! Eteğin aradığın bedeni STOĞA GİRDİ!\n\nBulunanlar: {bulunanlar_str}\n\nHemen tıkla: {URL}")
            else:
                print("Kontrol edildi: 34 ve 36 bedenler hala tükenmiş.")
        else:
            send_telegram_message("⚠️ DİKKAT: Defacto stok verisi (PRODUCT_DETAIL_SIZE_DATA) okunamadı.")
            
    except Exception as e:
        hata_mesaji = f"❌ KRİTİK HATA! Defacto stok botu hata aldı:\n\n{str(e)}"
        send_telegram_message(hata_mesaji)
    finally:
        driver.quit()

@app.route("/")
def home():
    # cron-job.org istek attığı an siteye takılmadan HEMEN 200 OK cevabı verilir
    # Selenium ise arka planda (Thread içinde) bağımsız çalışmaya başlar
    thread = Thread(target=background_stock_check)
    thread.start()
    
    return "Stok kontrolü arka planda başlatıldı!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
