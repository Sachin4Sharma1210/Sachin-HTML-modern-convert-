import telebot
import os, re, base64, random, string
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Render Fix ---
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

# --- Bot Config ---
BOT_TOKEN = "8772180534:AAGJby7G5cXHLb_VYr0Hh1Bz40DwsxacHvM"
bot = telebot.TeleBot(BOT_TOKEN)

# --- Logic ---
def extract_data(content):
    data = []
    for line in content.strip().split("\n"):
        if not line.strip(): continue
        for sep in [':', ' - ', '|', '=>', '->']:
            if sep in line:
                p = line.split(sep, 1)
                u = p[1].strip().strip('"').strip("'").strip()
                if "media-cdn.classplusapp.com" in u:
                    u = f"https://api.extractor.workers.dev/player?url={u}"
                data.append((p[0].strip(), u))
                break
    return data

def categorize(urls):
    v, p = [], []
    v_p = [r'\.m3u8', r'\.mp4', r'media-cdn', r'api\.extractor', r'youtube', r'youtu\.be', r'testbook']
    p_p = [r'\.pdf', r'/pdf/', r'drive\.google']
    for n, u in urls:
        if any(re.search(pat, u, re.IGNORECASE) for pat in v_p): v.append((n, u))
        elif any(re.search(pat, u, re.IGNORECASE) for pat in p_p): p.append((n, u))
    return v, p

def encode_url(url):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return base64.b64encode(base64.b64encode((salt + url).encode()).decode().encode()).decode()

def generate_html(f_name, v, p):
    title = os.path.splitext(f_name)[0]
    
    # आपकी भेजी हुई HTML फ़ाइल का प्रीमियम लॉजिक और डिज़ाइन
    template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>{0}</title>
    <link href="https://cdn.plyr.io/3.7.8/plyr.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        :root {{ --primary: #4299e1; --bg: #0f172a; --card: rgba(30, 41, 59, 0.7); }}
        body {{ background: var(--bg); color: #f8fafc; font-family: 'Inter', sans-serif; overflow-x: hidden; }}
        .navbar-brand {{ font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; }}
        .glass-card {{ background: var(--card); backdrop-filter: blur(12px); border-radius: 1.5rem; border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
        .video-wrapper {{ border-radius: 1rem; overflow: hidden; aspect-ratio: 16/9; background: #000; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.05); }}
        .search-container input {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 0.75rem; padding: 0.8rem 1.2rem; }}
        .list-group-item {{ background: rgba(255,255,255,0.03); color: white; border: 1px solid rgba(255,255,255,0.05); border-radius: 1rem !important; margin-bottom: 0.75rem; transition: 0.3s; cursor: pointer; }}
        .list-group-item:hover {{ transform: scale(1.02); background: rgba(66, 153, 225, 0.15); }}
        .nav-pills .nav-link.active {{ background: var(--primary); box-shadow: 0 4px 14px rgba(66, 153, 225, 0.4); }}
    </style>
</head>
<body class="py-4">
    <div class="container">
        <div class="text-center mb-4">
            <a href="https://t.me/Avigat1210" class="navbar-brand">⚡ SACHIN SHARMA ⚡</a>
            <p class="text-muted small mt-2">{0}</p>
        </div>

        <div class="glass-card mb-4">
            <div class="video-wrapper"><video id="player" playsinline controls></video></div>
            <div class="search-container"><input type="text" id="searchInput" class="form-control" placeholder="Search topics..." oninput="filterContent()"></div>
        </div>

        <div class="glass-card">
            <ul class="nav nav-pills nav-justified mb-4" role="tablist">
                <li class="nav-item"><a class="nav-link active" data-bs-toggle="tab" href="#vids"><i class="fas fa-video me-2"></i>Videos ({1})</a></li>
                <li class="nav-item"><a class="nav-link" data-bs-toggle="tab" href="#pdfs"><i class="fas fa-file-pdf me-2"></i>PDFs ({2})</a></li>
            </ul>
            <div class="tab-content">
                <div id="vids" class="tab-pane fade show active"><div class="list-group">{3}</div></div>
                <div id="pdfs" class="tab-pane fade"><div class="list-group">{4}</div></div>
            </div>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player');
        function de(s) {{ return atob(atob(s)).slice(8); }}
        function play(s) {{
            const u = de(s);
            if(Hls.isSupported() && u.includes('.m3u8')) {{
                const h = new Hls(); h.loadSource(u); h.attachMedia(document.querySelector('#player'));
            }} else {{
                player.source = {{ type:'video', sources:[{{src:u, type:'video/mp4'}}] }};
            }}
            player.play(); window.scrollTo({{top:0, behavior:'smooth'}});
        }}
        function view(s) {{ window.open('https://tempnewwebsite.classx.co.in/pdfjs/web/viewer.html?file=' + encodeURIComponent(de(s)), '_blank'); }}
        function filterContent() {{
            const s = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.list-group-item').forEach(i => {{
                i.style.display = i.innerText.toLowerCase().includes(s) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

    v_html = "".join([f'<div class="list-group-item" onclick="play(\'{encode_url(u)}\')"><i class="fas fa-play-circle me-3 text-primary"></i>{n}</div>' for n, u in v])
    p_html = "".join([f'<div class="list-group-item" onclick="view(\'{encode_url(u)}\')"><i class="fas fa-file-pdf me-3 text-danger"></i>{n}</div>' for n, u in p])

    return template.format(title, len(v), len(p), v_html, p_html)

# --- Bot Handlers ---
@bot.message_handler(commands=["start"])
def welcome(m):
    bot.reply_to(m, "✨ **Professional Text To HTML Bot**\n\nDirectly send me your `.txt` file.\n\n‡ 𝕮𝖗𝖊𝖆𝖙𝖊𝖉 𝕭𝖞: ➤ 𝕊𝔸ℂℍ𝕀ℕ 𝕊ℍ𝔸ℝ𝕄𝔸")

@bot.message_handler(content_types=['document'])
def handle_file(m):
    if not m.document.file_name.endswith('.txt'): return
    wait = bot.send_message(m.chat.id, "⚡ **Processing with Premium Logic...**")
    
    file_info = bot.get_file(m.document.file_id)
    content = bot.download_file(file_info.file_path).decode('utf-8')
    
    v, p = categorize(extract_data(content))
    html_data = generate_html(m.document.file_name, v, p)
    
    out_name = m.document.file_name.replace(".txt", "_@Sachin4Sharma1210.html")
    with open(out_name, "w", encoding='utf-8') as f: f.write(html_data)
    
    with open(out_name, "rb") as f:
        bot.send_document(m.chat.id, f, caption="✅ **HTML Generated Successfully!**\n\n**OPERATED BY SACHIN SHARMA**")
    
    os.remove(out_name)
    bot.delete_message(m.chat.id, wait.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

        else: o.append((n, u))
    return v, p, o

def obfuscate(url):
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return base64.b64encode(base64.b64encode((salt + url).encode()).decode().encode()).decode()

def generate_html(f_name, v, p, o):
    title = os.path.splitext(f_name)[0]
    
    # --- HTML TEMPLATE (No Backslash Error) ---
    template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{0}</title>
    <link href="https://cdn.plyr.io/3.7.8/plyr.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        :root[data-theme="dark"] {{ --bg: #0f172a; --text: #e2e8f0; --card: rgba(255, 255, 255, 0.1); --primary: #3b82f6; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; padding-bottom: 30px; }}
        .brand-title {{ font-size: 2.8rem; font-weight: 900; text-align: center; padding: 30px 10px; }}
        .brand-title a {{ background: linear-gradient(45deg, #3b82f6, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-decoration: none; text-transform: uppercase; letter-spacing: 2px; }}
        .glass-card {{ background: var(--card); backdrop-filter: blur(12px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); padding: 20px; margin: 15px auto; max-width: 900px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .player-box {{ aspect-ratio: 16/9; background: #000; border-radius: 15px; overflow: hidden; margin-bottom: 25px; border: 1px solid rgba(59,130,246,0.3); }}
        .search-bar {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 12px; padding: 15px; width: 100%; margin-bottom: 25px; font-size: 1.1rem; }}
        .list-group-item {{ background: rgba(255,255,255,0.03); color: white; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px !important; margin-bottom: 12px; padding: 15px 20px; cursor: pointer; display: flex; align-items: center; transition: 0.3s; }}
        .list-group-item:hover {{ background: rgba(59,130,246,0.2); transform: translateX(10px); border-color: var(--primary); }}
        .nav-tabs {{ border: none; justify-content: center; gap: 10px; margin-bottom: 20px; }}
        .nav-link {{ color: #94a3b8; font-weight: 700; border: none !important; border-radius: 10px !important; padding: 10px 25px; transition: 0.3s; }}
        .nav-link.active {{ background: var(--primary) !important; color: white !important; box-shadow: 0 5px 15px rgba(59,130,246,0.4); }}
        .floating-up {{ position: fixed; bottom: 25px; right: 25px; background: var(--primary); width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.3); z-index: 100; }}
    </style>
</head>
<body>
    <div class="brand-title">
        <a href="https://t.me/Avigat1210"><i class="fas fa-bolt"></i> SACHIN SHARMA <i class="fas fa-bolt"></i></a>
    </div>

    <div class="container">
        <div class="glass-card">
            <div class="player-box"><video id="videoPlayer" playsinline controls></video></div>
            <input type="text" class="search-bar" id="search" placeholder="🔎 Search content..." oninput="doSearch()">
            
            <ul class="nav nav-tabs" role="tablist">
                <li class="nav-item"><a class="nav-link active" data-bs-toggle="tab" href="#v">VIDEOS ({1})</a></li>
                <li class="nav-item"><a class="nav-link" data-bs-toggle="tab" href="#p">PDFS ({2})</a></li>
                <li class="nav-item"><a class="nav-link" data-bs-toggle="tab" href="#o">OTHERS ({3})</a></li>
            </ul>

            <div class="tab-content">
                <div id="v" class="tab-pane fade show active"><div class="list-group">{4}</div></div>
                <div id="p" class="tab-pane fade"><div class="list-group">{5}</div></div>
                <div id="o" class="tab-pane fade"><div class="list-group">{6}</div></div>
            </div>
        </div>
    </div>

    <div class="floating-up" onclick="window.scrollTo({{top:0, behavior:'smooth'}})">
        <i class="fas fa-chevron-up"></i>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const plyr = new Plyr('#videoPlayer', {{ settings:['quality','speed'], speed:{{selected:1, options:[0.5, 1, 1.25, 1.5, 2]}} }});
        function d(e) {{ return atob(atob(e)).slice(8); }}
        function playVideo(e) {{
            const u = d(e);
            if(Hls.isSupported() && u.includes('.m3u8')) {{
                const hls = new Hls(); hls.loadSource(u); hls.attachMedia(document.querySelector('#videoPlayer'));
            }} else {{
                plyr.source = {{ type:'video', sources:[{{src:u, type:'video/mp4'}}] }};
            }}
            plyr.play(); window.scrollTo({{top:0, behavior:'smooth'}});
        }}
        function viewPDF(e) {{ window.open('https://tempnewwebsite.classx.co.in/pdfjs/web/viewer.html?file=' + encodeURIComponent(d(e)), '_blank'); }}
        function doSearch() {{
            const s = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.list-group-item').forEach(i => {{
                i.style.display = i.innerText.toLowerCase().includes(s) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

    v_li = "".join([f'<div class="list-group-item" onclick="playVideo(\'{obfuscate(u)}\')"><i class="fas fa-play-circle me-3" style="color:#3b82f6"></i>{n}</div>' for n, u in v])
    p_li = "".join([f'<div class="list-group-item" onclick="viewPDF(\'{obfuscate(u)}\')"><i class="fas fa-file-pdf me-3 text-danger"></i>{n}</div>' for n, u in p])
    o_li = "".join([f'<div class="list-group-item" onclick="window.open(\'{u}\',\'_blank\')"><i class="fas fa-link me-3 text-success"></i>{n}</div>' for n, u in o])

    return template.format(title, len(v), len(p), len(o), v_li, p_li, o_li)

# --- Handlers ---
@bot.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith('.txt'): return
    wait = await m.reply_text("✨ Processing File... ⏳")
    path = await m.download()
    with open(path, "r", encoding='utf-8') as f: content = f.read()
    v, p, o = categorize(extract_names_and_urls(content))
    html_out = generate_html(m.document.file_name, v, p, o)
    name = m.document.file_name.replace(".txt", "_@Sachin4Sharma1210.html")
    with open(name, "w", encoding='utf-8') as f: f.write(html_out)
    await m.reply_document(name, caption="✅ **OPERATED BY SACHIN SHARMA**")
    os.remove(path); os.remove(name); await wait.delete()

if __name__ == "__main__":
    keep_alive()
    bot.run()

