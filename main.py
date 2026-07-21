import requests
import os
import json
import re

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def test_json_stok():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        
        # Sitenin kaynak kodundan PRODUCT_DETAIL_SIZE_DATA isimli JSON dizisini RegEx ile yakalıyoruz
        match = re.search(r'PRODUCT_DETAIL_SIZE_DATA\s*=\s*(\[.*?\]);', response.text)
        
        if match:
            json_data = match.group(1)
            stok_listesi = json.loads(json_data)
            
            mesaj = "🔍 Backend (JSON) Stok Raporu - Sadece Açık Pembe:\n\n"
            
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
            send_telegram_message("⚠️ JSON verisi bulunamadı. Defacto kod yapısını değiştirmiş olabilir.")
            
    except Exception as e:
        send_telegram_message(f"Bağlantı Hatası: {e}")

if __name__ == "__main__":
    test_json_stok()
