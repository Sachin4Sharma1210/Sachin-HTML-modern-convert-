import os
import re
import base64
import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message
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

# --- Bot Credentials ---
API_ID = 39218807
API_HASH = "5de693a30428272c34497419328466a1"
BOT_TOKEN = "8441306868:AAFiY_FTmyljnldJq6da8NcESkH5hVXCiLA"

bot = Client("sachin_html_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Original Logic ---
def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if not line.strip(): continue
        separators = [':', ' - ', '|', '=>', '->']
        for separator in separators:
            if separator in line:
                parts = line.split(separator, 1)
                name, url = parts[0].strip(), parts[1].strip().strip('"').strip("'").strip()
                if "media-cdn.classplusapp.com" in url:
                    url = f"https://api.extractor.workers.dev/player?url={url}"
                data.append((name, url))
                break
    return data

def categorize_urls(urls):
    videos, pdfs, others = [], [], []
    v_pat = [r'\.m3u8', r'\.mp4', r'media-cdn', r'api\.extractor', r'youtube', r'youtu\.be']
    p_pat = [r'\.pdf', r'/pdf/', r'drive\.google', r'docs\.google']
    for name, url in urls:
        if any(re.search(p, url, re.IGNORECASE) for p in v_pat): videos.append((name, url))
        elif any(re.search(p, url, re.IGNORECASE) for p in p_pat): pdfs.append((name, url))
        else: others.append((name, url))
    return videos, pdfs, others

def obfuscate_url(url):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    encoded = base64.b64encode(base64.b64encode((salt + url).encode()).decode().encode()).decode()
    return encoded

def generate_html(file_name, videos, pdfs, others):
    title = os.path.splitext(file_name)[0]
    # HTML template started
    html_code = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.plyr.io/3.7.8/plyr.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        :root[data-theme="dark"] {{ --bs-body-bg: #0f172a; --bs-body-color: #e2e8f0; --card-bg: rgba(255, 255, 255, 0.1); }}
        body {{ background: var(--bs-body-bg); color: var(--bs-body-color); font-family: 'Inter', sans-serif; }}
        .brand-title {{ font-size: 2.5rem; font-weight: 900; text-align: center; padding: 20px; }}
        .brand-title a {{ background: linear-gradient(45deg, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-decoration: none; text-transform: uppercase; }}
        .glass-card {{ background: var(--card-bg); backdrop-filter: blur(16px); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); padding: 15px; margin: 10px; }}
        .video-container {{ aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden; }}
        .search-input {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 10px; padding: 12px; width: 100%; margin-bottom: 20px; }}
        .list-group-item {{ background: rgba(255,255,255,0.05); color: white; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; cursor: pointer; display: flex; align-items: center; padding: 12px; }}
    </style>
</head>
<body>
    <div class="brand-title"><a href="https://t.me/Avigat1210">SACHIN SHARMA</a></div>
    <div class="container mb-4"><div class="glass-card"><div class="video-container"><video id="player" playsinline controls></video></div></div></div>
    <div class="container">
        <div class="glass-card">
            <input type="text" class="search-input" id="searchInput" placeholder="Search..." oninput="filterContent()">
            <ul class="nav nav-tabs mb-3" role="tablist">
                <li class="nav-item"><a class="nav-link active" data-bs-toggle="tab" href="#vids">Videos ({len(videos)})</a></li>
                <li class="nav-item"><a class="nav-link" data-bs-toggle="tab" href="#pfs">PDFs ({len(pdfs)})</a></li>
            </ul>
            <div class="tab-content">
                <div id="vids" class="tab-pane fade show active"><div class="list-group">{"".join([f'<div class="list-group-item" onclick="playVideo(\'{obfuscate_url(u)}\')">{n}</div>' for n, u in videos])}</div></div>
                <div id="pfs" class="tab-pane fade"><div class="list-group">{"".join([f'<div class="list-group-item" onclick="viewPDF(\'{obfuscate_url(u)}\')">{n}</div>' for n, u in pdfs])}</div></div>
            </div>
        </div>
    </div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player');
        function deob(enc) {{ return atob(atob(enc)).slice(8); }}
        function playVideo(enc) {{
            const url = deob(enc);
            if (Hls.isSupported() && url.includes('.m3u8')) {{
                const hls = new Hls(); hls.loadSource(url); hls.attachMedia(document.querySelector('#player'));
            }} else {{
                player.source = {{ type: 'video', sources: [{{ src: url, type: 'video/mp4' }}] }};
            }}
            player.play();
        }}
        function viewPDF(enc) {{ window.open(`https://tempnewwebsite.classx.co.in/pdfjs/web/viewer.html?file=${{encodeURIComponent(deob(enc))}}`, '_blank'); }}
        function filterContent() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.list-group-item').forEach(item => {{ item.style.display = item.innerText.toLowerCase().includes(search) ? '' : 'none'; }});
        }}
    </script>
</body>
</html>"""
    return html_code

@bot.on_message(filters.document)
async def handle_txt(client, message):
    if not message.document.file_name.endswith('.txt'): return
    proc = await message.reply_text("Processing... ⏳")
    path = await message.download()
    with open(path, "r", encoding='utf-8') as f: content = f.read()
    v, p, o = categorize_urls(extract_names_and_urls(content))
    html_data = generate_html(message.document.file_name, v, p, o)
    out = message.document.file_name.replace(".txt", "_@Sachin4Sharma1210.html")
    with open(out, "w", encoding='utf-8') as f: f.write(html_data)
    await message.reply_document(out, caption="✅ **OPERATED BY SACHIN SHARMA**")
    os.remove(path); os.remove(out); await proc.delete()

if __name__ == "__main__":
    keep_alive()
    bot.run()

