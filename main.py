import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def check_stock_selenium():
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
            hedef_bedenler = ["34", "36"]
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
            print("Uyarı: Veri okunamadı.")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_stock_selenium()
