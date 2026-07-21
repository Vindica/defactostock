import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def test_selenium_bot():
    # Görünmez bir Chrome tarayıcısı yapılandırıyoruz
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Tarayıcı arayüzü olmadan çalış
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(URL)
        # JavaScript'in çalışıp API'den beden listesini getirmesi için 5 saniye bekliyoruz
        time.sleep(5) 
        
        # Sayfadaki tüm görünür metinleri çekiyoruz (Distill eklentisinin okuduğu formatta)
        sayfa_metni = driver.find_element(By.TAG_NAME, "body").text
        
        mesaj = "🤖 Selenium Tarayıcısından Çekilen Veriler:\n\n"
        
        # Distill ekran görüntülerinde gördüğümüz mantığı uyguluyoruz: 
        # Bedenin yanında "Benzerini Gör" yazıyorsa tükenmiştir.
        bedenler = ["34", "36", "38", "40", "42"]
        sayfa_metni_tek_satir = sayfa_metni.replace('\n', ' ')
        
        for beden in bedenler:
            # "34 Benzerini Gör" yan yana veya alt alta gelmiş mi kontrol ediyoruz
            if f"{beden}\nBenzerini Gör" in sayfa_metni or f"{beden} Benzerini Gör" in sayfa_metni_tek_satir:
                mesaj += f"❌ {beden} Beden: Tükendi\n"
            elif str(beden) in sayfa_metni:
                mesaj += f"✅ {beden} Beden: STOKTA VAR!\n"
            else:
                mesaj += f"⚠️ {beden} Beden: Ekranda hiç bulunamadı.\n"
                
        send_telegram_message(mesaj)
        
    except Exception as e:
        send_telegram_message(f"Hata oluştu: {e}")
    finally:
        driver.quit() # Sistemi yormamak için Chrome'u kapatıyoruz

if __name__ == "__main__":
    test_selenium_bot()
