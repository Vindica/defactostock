import requests
import os

TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')

def test_mesaji_gonder():
    print("Telegram'a bağlanmaya çalışıyorum...")
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Telegram'a mesaj atıyoruz ve verdiği cevabı ekrana yazdırıyoruz
    response = requests.post(api_url, data={'chat_id': CHAT_ID, 'text': "Merhaba! Bağlantı başarılı! 🚀"})
    
    print(f"Telegram'ın Cevabı: {response.text}")

if __name__ == "__main__":
    test_mesaji_gonder()
