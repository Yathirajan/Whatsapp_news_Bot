import requests
import time
from twilio.rest import Client

NEWSDATA_API_KEY = "apikey"
TWILIO_SID = "yourkey"
Topic="Top Sports News"
TWILIO_AUTH_TOKEN = "your token"
FROM_WHATSAPP_NUMBER = "whatsapp:+14155238886"
TO_WHATSAPP_NUMBER = "whatsapp:your number"

clients = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def get_latest_news():
    url = (
     f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={Topic.replace(' ', '%20')}&country=in&language=en" 
    )
    response = requests.get(url)
    data = response.json()
    if data.get("status") == "success" and data.get("results"):
        messages = []
        for article in data["results"][:3]:
            title = article["title"]
            source = article.get("source_id", "Unknown")
            pub_date = article["pubDate"]
            link = article["link"]
            messages.append(f"🗞️ *{title}*\n📍{source} | 🕒 {pub_date}\n🔗 {link}")
        return "\n\n".join(messages)
    return "⚠️ No news found."

def send_whatsapp_message(message):
    clients.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        body=message,
        to=TO_WHATSAPP_NUMBER
    )

while True:
    news = get_latest_news()
    send_whatsapp_message(news)
    time.sleep(3600)  # Sleep for 1 hour (3600 seconds)