import os
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Render Fix (Web Server) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()

# --- बोट डिटेल्स ---
API_ID = 39218807
API_HASH = "5de693a30428272c34497419328466a1"
BOT_TOKEN = "8772180534:AAGJby7G5cXHLb_VYr0Hh1Bz40DwsxacHvM"

bot = Client("html_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HTML कनवर्टर लॉजिक ---
def extract_links(content):
    # यह आपके वीडियो वाले फॉर्मेट (Name - Link) को सपोर्ट करेगा
    pattern = re.compile(r'(.+?)\s*[-:]\s*(https?://\S+)')
    return pattern.findall(content)

def generate_html(file_name, links):
    link_rows = "".join([
        f"<tr><td>{name}</td><td><a href='{url}' target='_blank'>🔗 𝐕𝐢𝐞𝐰 𝐍𝐨𝐰</a></td></tr>" 
        for name, url in links
    ])
    
    return f"""<!doctype html>
<html>
<head>
    <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap' rel='stylesheet'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
        body {{ font-family: 'Poppins', sans-serif; text-align: center; margin: 0; background-color: #0f0120; color: white; }}
        table {{ width: 95%; margin: 20px auto; border-collapse: collapse; background: white; color: black; border-radius: 10px; overflow: hidden; }}
        th, td {{ padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #f87b06; color: white; }}
        a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>➤ <a href="https://t.me/Avigat1210" style="color:white; text-decoration:none;">𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸</a></h1>
    <h3>{file_name}</h3>
    <table>
        <tr><th>Topic</th><th>Action</th></tr>
        {link_rows}
    </table>
</body>
</html>"""

# --- बोट कमांड्स ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"**नमस्ते {message.from_user.first_name}!**\nमैं .txt फ़ाइल को आधुनिक HTML में बदल सकता हूँ।",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 चैनल", url="https://t.me/Sachin4Sharma1210"),
             InlineKeyboardButton("👨‍💻 ओनर", url="https://t.me/Avigat1210")]
        ])
    )

@bot.on_message(filters.document & filters.private)
async def handle_txt(client, message):
    if not message.document.file_name.endswith(".txt"):
        return await message.reply_text("❌ कृपया केवल .txt फाइल भेजें।")

    msg = await message.reply_text("⏳ आधुनिक डिजाइन में कनवर्ट कर रहा हूँ...")
    file_path = await message.download()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    links = extract_links(content)
    if not links:
        await msg.edit("❌ फाइल में कोई लिंक नहीं मिला!")
        return os.remove(file_path)

    html_name = message.document.file_name.replace(".txt", ".html")
    html_content = generate_html(message.document.file_name, links)
    
    with open(html_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    await message.reply_document(html_name, caption="✅ **HTML कनवर्ट हो गया!**\n‡ 𝕮𝖗𝖊𝖆𝖙𝖊𝖉 𝕭𝖞: ➤ 𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸")
    await msg.delete()
    
    # सफाई
    os.remove(file_path)
    os.remove(html_name)

if __name__ == "__main__":
    keep_alive()
    bot.run()
