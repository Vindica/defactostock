import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests_post(api_url, data={'chat_id': CHAT_ID, 'text': text})

# Not: requests kütüphanesi yerine selenium içi requests kullanıyorsak urllib da kullanılabilir, 
# ancak requests zaten yukarIDA import edilebiliyor. Ufak bir düzeltme yapalım:
import requests

def check_stock_and_notify():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(URL)
        time.sleep(4) # Sayfanın yüklenmesi için bekleme
        
        # Sitenin hafızasından gerçek stok verisini çekiyoruz
        stok_listesi = driver.execute_script("return PRODUCT_DETAIL_SIZE_DATA;")
        
        if stok_listesi:
            hedef_bedenler = ["34", "36"]
            stoka_girenler = []
            
            for beden_bilgisi in stok_listesi:
                beden = beden_bilgisi.get("Size")
                stok_miktari = beden_bilgisi.get("StockQuantity", 0)
                
                # Eğer aradığımız 34 veya 36 bedenin stoğu 0'dan büyükse listeye ekle
                if beden in hedef_bedenler and stok_miktari > 0:
                    stoka_girenler.append(f"{beden} Beden (Kalan: {stok_miktari})")
            
            # Eğer stokta olan aradığımız beden varsa ANINDA alarm gönder!
            if stoka_girenler:
                bulunanlar_str = ", ".join(stoka_girenler)
                mesaj = f"🚨 MÜJDE! Eteğin aradığın bedeni STOĞA GİRDİ!\n\nBulunanlar: {bulunanlar_str}\n\nHemen tıkla: {URL}"
                send_telegram_message(mesaj)
            else:
                print("Kontrol edildi: Aranan 34 ve 36 bedenler hala tükenmiş durumda. Sessizce bekleniyor...")
                
        else:
            print("Uyarı: Stok verisi okunamadı.")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_stock_and_notify()
