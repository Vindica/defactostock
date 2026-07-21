import requests
import os

# GitHub Secrets'tan API anahtarlarını çekiyoruz
TOKEN = os.environ.get('TELE_TOKEN')
CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = "https://www.defacto.com.tr/normal-bel-pamuk-astarli-krinkil-kumas-maxi-etek-3445374"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(URL, headers=headers)
    
    # HTML kodunun içinde 34 veya 36 bedenin 'tükendi' ibaresinin olup olmadığını kontrol ediyoruz.
    # Bu basit bir string eşleştirmesidir. Stok geldiğinde 'Benzerini Gör' veya 'is-no-stock' kodları kalkar.
    
    if "SEÇİLEN RENK:" in response.text: # Sayfanın doğru yüklendiğini teyit ediyoruz
        # Defacto kaynak kodunda stoksuz bedenler genellikle spesifik sınıflarla işaretlenir.
        # Eğer stok varsa, doğrudan bedeni sepete ekleme aktif olur.
        # Çok basit bir mantık: 34 bedenin stoksuz kodu sayfada YOKA stok gelmiştir.
        
        # Not: Sitenin HTML yapısına göre bu if bloğundaki metinler optimize edilebilir.
        if 'data-size="34"' in response.text and 'disabled' not in response.text:
            send_telegram_message(f"🚨 ETEK STOĞA GİRDİ! Hemen tıkla: {URL}")
            
if __name__ == "__main__":
    check_stock()
