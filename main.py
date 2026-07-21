import os
import requests
import json
import re

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def check_stock_json():
    # Defacto'nun bot korumasını atlatmak için güncel bir Tarayıcı (User-Agent) başlığı kullanıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        
        # Sayfanın kaynak kodundan PRODUCT_DETAIL_SIZE_DATA dizisini yakalıyoruz
        match = re.search(r'PRODUCT_DETAIL_SIZE_DATA\s*=\s*(\[.*?\]);', response.text)
        
        if match:
            json_data = match.group(1)
            stok_listesi = json.loads(json_data)
            
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
            print("Uyarı: JSON verisi eşleşmedi, site yapısı kontrol edilmeli.")
            
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")

if __name__ == "__main__":
    check_stock_json()
