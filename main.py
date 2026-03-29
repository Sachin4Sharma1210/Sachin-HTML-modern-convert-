import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask Server for Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- बोट कॉन्फ़िगरेशन ---
# ये वैल्यूज आप Render के Environment Variables में भी डाल सकते हैं
API_ID = 39218807
API_HASH = "5de693a30428272c34497419328466a1"
BOT_TOKEN = "8772180534:AAGJby7G5cXHLb_VYr0Hh1Bz40DwsxacHvM"

bot = Client(
    "html_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- स्टार्ट कमांड ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = f"हेलो {message.from_user.first_name}!\n\nमैं एक **Advanced HTML Converter** बोट हूँ।\nअपनी `.txt` फाइल भेजें।"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 चैनल", url="https://t.me/Sachin4Sharma1210"),
         InlineKeyboardButton("👨‍💻 ओनर", url="https://t.me/Avigat1210")]
    ])
    await message.reply_text(text, reply_markup=reply_markup)

# --- फाइल हैंडलर (यहाँ आपका कनवर्टर लॉजिक आएगा) ---
@bot.on_message(filters.document & filters.private)
async def handle_document(client, message):
    if message.document.file_name.endswith(".txt"):
        msg = await message.reply_text("⏳ फाइल प्रोसेस हो रही है...")
        
        # फाइल डाउनलोड करें
        file_path = await message.download()
        
        # यहाँ आप अपनी 'bot_pay.py' या 'botenc.py' के फंक्शन कॉल कर सकते हैं
        # अभी के लिए यह सिर्फ एक उदाहरण है:
        html_path = file_path.replace(".txt", ".html")
        
        # (HTML बनाने का लॉजिक यहाँ लिखें या अपनी दूसरी फाइल से इम्पोर्ट करें)
        
        try:
            # फाइल वापस भेजें
            await message.reply_document(file_path) # उदाहरण के लिए वही फाइल
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ एरर: {str(e)}")
        
        # सफाई (फाइल डिलीट करना)
        if os.path.exists(file_path): os.remove(file_path)
    else:
        await message.reply_text("❌ कृपया केवल .txt फाइल भेजें।")

# --- बोट रन करें ---
if __name__ == "__main__":
    keep_alive()
    print("Pyrogram Bot started...")
    bot.run()

