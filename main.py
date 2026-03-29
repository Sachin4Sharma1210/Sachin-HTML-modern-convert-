import os
import re
import base64
import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

# --- Render Timeout Fix (Web Server) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive and Running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- Bot Credentials ---
API_ID = 39218807
API_HASH = "5de693a30428272c34497419328466a1"
BOT_TOKEN = "8441306868:AAFiY_FTmyljnldJq6da8NcESkH5hVXCiLA"

bot = Client("sachin_html_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Link Extraction Logic ---
def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if not line.strip(): continue
        separators = [':', ' - ', '|', '=>', '->']
        for separator in separators:
            if separator in line:
                parts = line.split(separator, 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    url = parts[1].strip().strip('"').strip("'").strip()
                    if "media-cdn.classplusapp.com" in url:
                        url = f"https://api.extractor.workers.dev/player?url={url}"
                    data.append((name, url))
                    break
    return data

def categorize_urls(urls):
    videos, pdfs, others = [], [], []
    video_patterns = [r'\.m3u8', r'\.mp4', r'media-cdn\.classplusapp\.com', r'api\.extractor\.workers\.dev', r'cpvod\.testbook', r'/master\.mpd', r'youtube\.com', r'youtu\.be']
    pdf_patterns = [r'\.pdf', r'/pdf/', r'drive\.google\.com.*pdf']
    for name, url in urls:
        if any(re.search(p, url, re.IGNORECASE) for p in video_patterns): videos.append((name, url))
        elif any(re.search(p, url, re.IGNORECASE) for p in pdf_patterns): pdfs.append((name, url))
        else: others.append((name, url))
    return videos, pdfs, others

# --- HTML Generator (Original Modern UI) ---
def generate_html(file_name, videos, pdfs, others):
    file_title = os.path.splitext(file_name)[0]
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en" data-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{file_title}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
        <style>
            :root {{ --primary: #3b82f6; --bg: #0f172a; --card: #1e293b; --text: #f8fafc; }}
            body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; padding-bottom: 50px; }}
            .brand-header {{ padding: 50px 0; text-align: center; background: linear-gradient(180deg, rgba(59,130,246,0.15) 0%, rgba(15,23,42,0) 100%); }}
            .brand-title {{ font-size: 3.5rem; font-weight: 900; letter-spacing: 3px; color: var(--primary); margin-bottom: 10px; text-shadow: 0 0 20px rgba(59,130,246,0.5); }}
            .operator-tag {{ font-size: 1.2rem; font-weight: 700; color: #ff9800; text-decoration: none; text-transform: uppercase; padding: 10px 20px; border: 2px solid #ff9800; border-radius: 50px; transition: 0.3s; display: inline-block; }}
            .operator-tag:hover {{ background: #ff9800; color: #fff; box-shadow: 0 0 20px rgba(255,152,0,0.4); }}
            .glass-card {{ background: var(--card); border: 1px solid rgba(255,255,255,0.1); border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); padding: 30px; margin-top: -30px; }}
            .list-item {{ display: flex; align-items: center; padding: 18px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 15px; margin-bottom: 15px; transition: 0.4s; text-decoration: none; color: white; }}
            .list-item:hover {{ background: rgba(59,130,246,0.2); border-color: var(--primary); transform: translateY(-3px); }}
            .icon-box {{ width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; background: rgba(59,130,246,0.2); border-radius: 12px; margin-right: 20px; color: var(--primary); font-size: 1.3rem; }}
            .item-name {{ font-size: 1.1rem; font-weight: 600; flex: 1; }}
            .section-title {{ margin: 40px 0 20px; font-size: 1.3rem; font-weight: 800; color: #64748b; text-transform: uppercase; border-left: 5px solid var(--primary); padding-left: 15px; }}
        </style>
    </head>
    <body>
        <div class="brand-header">
            <h1 class="brand-title">SACHIN SHARMA</h1>
            <a href="https://t.me/Avigat1210" target="_blank" class="operator-tag">OPERATED BY SACHIN SHARMA</a>
        </div>
        <div class="container">
            <div class="glass-card">
                <h3 class="text-center mb-5" style="color: #94a3b8;">{file_title}</h3>
                {"<div class='section-title'>🎬 Video Content</div>" if videos else ""}
                {"".join([f'<a href="{u}" target="_blank" class="list-item"><div class="icon-box"><i class="fas fa-play"></i></div><div class="item-name">{n}</div></a>' for n, u in videos])}
                {"<div class='section-title'>📄 PDF Documents</div>" if pdfs else ""}
                {"".join([f'<a href="{u}" target="_blank" class="list-item"><div class="icon-box"><i class="fas fa-file-pdf"></i></div><div class="item-name">{n}</div></a>' for n, u in pdfs])}
                {"<div class='section-title'>🔗 Other Links</div>" if others else ""}
                {"".join([f'<a href="{u}" target="_blank" class="list-item"><div class="icon-box"><i class="fas fa-link"></i></div><div class="item-name">{n}</div></a>' for n, u in others])}
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

# --- Bot Handlers ---
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"<b>नमस्ते {message.from_user.first_name}! 👋</b>\n\nमैं TXT को मॉडर्न HTML में बदलता हूँ। अपनी .txt फाइल भेजें।\n\n<b>Operated by Sachin Sharma</b>")

@bot.on_message(filters.document)
async def handle_document(client, message):
    if not message.document.file_name.endswith('.txt'): return
    
    status = await message.reply_text("फाइल प्रोसिस हो रही है... ⏳")
    path = await message.download()
    
    with open(path, "r", encoding='utf-8') as f:
        content = f.read()
    
    urls = extract_names_and_urls(content)
    if not urls:
        await status.edit("फाइल में कोई सही लिंक नहीं मिला!")
        return
        
    videos, pdfs, others = categorize_urls(urls)
    full_html = generate_html(message.document.file_name, videos, pdfs, others)
    
    output_name = message.document.file_name.replace(".txt", "_Modern.html")
    with open(output_name, "w", encoding='utf-8') as f:
        f.write(full_html)

    await message.reply_document(output_name, caption="✅ HTML फाइल तैयार है!\n\n<b>OPERATED BY SACHIN SHARMA</b>\n🔗 Join: @Avigat1210")
    
    os.remove(path)
    os.remove(output_name)
    await status.delete()

if __name__ == "__main__":
    keep_alive()
    bot.run()
    
