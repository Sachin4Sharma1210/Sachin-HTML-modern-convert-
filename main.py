import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- आपकी Extractor फाइलों को यहाँ से बुलाया जा रहा है ---
from Extractor.bot import handle_txt2html, show_txt2html_help

# --- Render Fix (Web Server) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive with Sachin's UI!"

def run_flask():
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 8080))

def keep_alive():
    Thread(target=run_flask, daemon=True).start()

# --- बोट कॉन्फ़िगरेशन (Render Environment Variables से उठाएगा) ---
API_ID = int(os.environ.get("API_ID", "39218807"))
API_HASH = os.environ.get("API_HASH", "5de693a30428272c34497419328466a1")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8772180534:AAGJby7G5cXHLb_VYr0Hh1Bz40DwsxacHvM")

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- बोट कमांड्स ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # यह आपके Extractor/bot.py वाले हेल्प मैसेज को दिखाएगा
    await show_txt2html_help(client, message)

@bot.on_message(filters.document & filters.private)
async def handle_document(client, message):
    # यह आपकी ओरिजिनल UI वाला कनवर्टर चलाएगा
    await handle_txt2html(client, message)

if __name__ == "__main__":
    keep_alive()
    print("Sachin Sharma's Bot is Starting...")
    bot.run()

