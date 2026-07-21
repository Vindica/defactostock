import requests
import os

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def test_stock_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        mesaj = "🔍 Siteden Çekilen Anlık Ham Veriler:\n\n"
        
        # Kontrol edilecek bedenler
        bedenler = ["34", "36", "38", "40", "42"]
        
        for beden in bedenler:
            hedef_kelime = f'data-size="{beden}"'
            
            if hedef_kelime in response.text:
                # O bedene ait HTML bloğunu kesip alıyoruz
                blok = response.text.split(hedef_kelime)[1][:150]
                
                # Sitenin stoksuz ürünlere koyduğu 'is-no-stock' etiketini arıyoruz
                if 'is-no-stock' in blok:
                    mesaj += f"❌ {beden} Beden: Tükendi ('is-no-stock' tespit edildi)\n"
                else:
                    mesaj += f"✅ {beden} Beden: STOKTA VAR!\n"
            else:
                mesaj += f"⚠️ {beden} Beden: Kod içinde hiç bulunamadı.\n"
                
        # Topladığımız raporu Telegram'a atıyoruz
        send_telegram_message(mesaj)
        
    except Exception as e:
        send_telegram_message(f"Bağlantı Hatası: {e}")

if __name__ == "__main__":
    test_stock_data()
