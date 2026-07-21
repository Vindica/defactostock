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

def test_stok_selenium_json():
    # Görünmez Chrome tarayıcımızı ayarlıyoruz
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(URL)
        time.sleep(3) # Sayfanın arka plan verilerinin yüklenmesi için kısa bir bekleme
        
        # İŞTE ALTIN VURUŞ: Selenium üzerinden sitenin kendi JS değişkenini doğrudan Python'a alıyoruz!
        stok_listesi = driver.execute_script("return PRODUCT_DETAIL_SIZE_DATA;")
        
        if stok_listesi:
            mesaj = "🎯 Kusursuz Stok Raporu - Sadece Açık Pembe:\n\n"
            
            # JSON (Sözlük) yapısının içinde dönüp stok miktarlarını okuyoruz
            for beden_bilgisi in stok_listesi:
                beden = beden_bilgisi.get("Size")
                stok_miktari = beden_bilgisi.get("StockQuantity", 0)
                
                if beden in ["34", "36", "38", "40", "42"]:
                    if stok_miktari > 0:
                        mesaj += f"✅ {beden} Beden: STOKTA VAR! (Kalan: {stok_miktari})\n"
                    else:
                        mesaj += f"❌ {beden} Beden: Tükendi\n"
                        
            send_telegram_message(mesaj)
        else:
            send_telegram_message("⚠️ Değişken bulunamadı veya sayfa yüklenemedi.")
            
    except Exception as e:
        send_telegram_message(f"Bağlantı Hatası: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_stok_selenium_json()
