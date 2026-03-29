import telebot
import os
import re
import random
import time
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Render Fix (Web Server) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- आपकी डिटेल्स ---
OWNER_ID = 7850454902
API_ID = 39218807
API_HASH = "5de693a30428272c34497419328466a1"
BOT_TOKEN = "8772180534:AAGJby7G5cXHLb_VYr0Hh1Bz40DwsxacHvM"

bot = telebot.TeleBot(BOT_TOKEN)

# --- फंक्शन्स ---

def extract_links(content):
    pattern = re.compile(r'(.+?)\s*[-:]\s*(https?://\S+)')
    return pattern.findall(content)

def txt_to_html(txt_path, html_path):
    file_name = os.path.basename(txt_path).replace('.txt', '')
    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        content = txt_file.read()

    links = extract_links(content)
    if not links:
        return None

    link_rows = "".join([
        f"<tr><td>{name}</td><td><a href='{url}' target='_blank'>🔗 𝐕𝐢𝐞𝐰 𝐍𝐨𝐰</a></td></tr>" 
        for name, url in links
    ])
    
    html_content = f"""<!doctype html>
<html>
<head>
    <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap' rel='stylesheet'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>{file_name}</title>
    <style>
        body {{ font-family: 'Poppins', sans-serif; text-align: center; margin: 0; background-color: #0f0120; color: white; }}
        table {{ width: 95%; margin: 20px auto; border-collapse: collapse; background: white; color: black; border-radius: 10px; overflow: hidden; }}
        th, td {{ padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #f87b06; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
        .footer {{ background: linear-gradient(to right, #f5f37a, #f1c480); color: black; padding: 15px; font-weight: bold; margin-top: 20px; }}
        h1 a {{ color: white; text-decoration: none; }}
    </style>
</head>
<body>
    <div style="margin: 20px 0;">
        <img src="https://envs.sh/tOz.jpg" height="150" style="border-radius: 10px;">
    </div>
    <h1>➤ <a href="https://t.me/Avigat1210">𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸</a></h1>
    <h3>{file_name}</h3>
    <table>
        <tr><th>Topic</th><th>Action</th></tr>
        {link_rows}
    </table>
    <div class='footer'>Developed By: ➤ <a href="https://t.me/Avigat1210" style="color:black; text-decoration:none;">𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸</a></div>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📢 Channel", url="https://t.me/Sachin4Sharma1210"),
        InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Avigat1210")
    )
    return keyboard

# --- बोट कमांड्स ---

@bot.message_handler(commands=["start"])
def start_command(message):
    caption = (
        f"**Hello {message.from_user.first_name} 👋!**\n\n"
        "➠ I am a **Text To HTML Bot**\n"
        "➠ Send your .txt file directly to convert.\n\n"
        "‡ 𝕮𝖗𝖊𝖆𝖙𝖊𝖉 𝕭𝖞: ➤ 𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸"
    )
    bot.send_photo(message.chat.id, "https://files.catbox.moe/v03e90.jpg", caption=caption, parse_mode="Markdown", reply_markup=start_keyboard())

@bot.message_handler(content_types=['document'])
def handle_txt_file(message):
    if not message.document.file_name.endswith('.txt'):
        bot.reply_to(message, "❌ Please send only .txt files.")
        return

    wait_msg = bot.send_message(message.chat.id, "⏳ Processing...")
    
    try:
        file_info = bot.get_file(message.document.file_id)
import asyncio
import importlib
import signal
from pyrogram import idle
from Extractor.modules import ALL_MODULES

loop = asyncio.get_event_loop()

# Graceful shutdown
should_exit = asyncio.Event()

def shutdown():
    print("Shutting down gracefully...")
    should_exit.set()  # triggers exit from idle

signal.signal(signal.SIGTERM, lambda s, f: loop.create_task(should_exit.set()))
signal.signal(signal.SIGINT, lambda s, f: loop.create_task(should_exit.set()))

async def sumit_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + all_module)

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    await idle()  # keeps the bot alive

    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

if __name__ == "__main__":
    try:
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Cancel pending tasks to avoid "destroyed but pending" error
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()
        print("Loop closed.")
