from flask import Flask, render_template_string, jsonify, request
import os
import hashlib
import time
import json
import requests
import threading

app = Flask(__name__)

# =====================================================================
# ⚙️ KONFIGURASI DUOGUARD SOC SENTINEL (DARI SOURCE 1)
# =====================================================================
FAIL_DILINDUNGI = {
    "config.json": "config.json",
    "cert_key.pem": "cert_key.pem",
    "cert.pem": "cert.pem",
    "dashboard.py": "dashboard.py",  # Dipantau secara terus di Render
    "README.md": "README.md",
    "requirements.txt": "requirements.txt"
}
FAIL_DATABASE_HASH = "duoguard_hashes.json"

TELEGRAM_TOKEN = "7964651809:AAFXMrLDM2d5A6hAYpsisIZguIDnJvvfFWU"
TELEGRAM_CHAT_ID = "6065278352"

# Pembolehubah global untuk dashboard membaca data live
DATA_MATRIX_GLOBAL = {
    "soc": {},
    "miner_status": "RUNNING",
    "hashrate_sekarang": "125 H/s"
}

def hantar_amaran_telegram(mesej):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesej, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[!] Gagal menghantar isyarat Telegram: {e}")

def kira_sha256(jalan_fail):
    hashing = hashlib.sha256()
    try:
        with open(jalan_fail, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hashing.update(chunk)
        return hashing.hexdigest()
    except FileNotFoundError:
        return None

# =====================================================================
# 🛡️ LOOP PEMANTAUAN BACKGROUND THREAD (AUTOMATIK SYNC DATA)
# =====================================================================
def jalankan_integrity_sentinel():
    print("[+] Mengesahkan integrity baseline di dalam Render server...")
    database_hash = {}
    
    if os.path.exists(FAIL_DATABASE_HASH):
        try:
            with open(FAIL_DATABASE_HASH, 'r') as f:
                database_hash = json.load(f)
        except:
            database_hash = {}

    for label_fail, jalan_fail in FAIL_DILINDUNGI.items():
        if os.path.exists(jalan_fail):
            hash_semasa = kira_sha256(jalan_fail)
            if jalan_fail not in database_hash:
                database_hash[jalan_fail] = hash_semasa
        else:
            # Letakkan placeholder jika fail belum wujud di Render
            database_hash[jalan_fail] = "FILE_NOT_FOUND_YET"

    with open(FAIL_DATABASE_HASH, 'w') as f:
        json.dump(database_hash, f, indent=4)
        
    # Masukkan terus ke dalam global matrix untuk paparan dashboard
    DATA_MATRIX_GLOBAL['soc'] = database_hash
    
    hantar_amaran_telegram("🚀 *DuoGuard SOC Cloud Alert*\n`Integrity Sentinel (Embedded Mode)` berjaya dilancarkan terus dalam kluster Render!")
    
    while True:
        try:
            time.sleep(10) # Semak setiap 10 saat (Lebih mesra CPU Render Free)
            database_semasa = {}
            if os.path.exists(FAIL_DATABASE_HASH):
                with open(FAIL_DATABASE_HASH, 'r') as f:
                    database_semasa = json.load(f)
            
            perubahan_dikesan = False
            
            for jalan_fail, hash_asal in list(database_semasa.items()):
                if not os.path.exists(jalan_fail):
                    if hash_asal != "FILE_NOT_FOUND_YET":
                        hantar_amaran_telegram(f"🚨 *DUOGUARD CLOUD WARNING!*\n\nFail kritikal di server Render telah *DIPADAMKAN*:\n📂 `{jalan_fail}`")
                        database_semasa[jalan_fail] = "FILE_NOT_FOUND_YET"
                        perubahan_dikesan = True
                    continue
                
                hash_semasa = kira_sha256(jalan_fail)
                if hash_asal == "FILE_NOT_FOUND_YET" or hash_semasa != hash_asal:
                    hantar_amaran_telegram(
                        f"🚨 *DUOGUARD CLOUD MODIFICATION!*\n\n"
                        f"Perubahan fail dikesan pada hos Render!\n"
                        f"📂 *Fail:* `{jalan_fail}`\n"
                        f"🔺 *Hash Baharu:* `{hash_semasa[:15]}...`"
                    )
                    database_semasa[jalan_fail] = hash_semasa
                    perubahan_dikesan = True

            if perubahan_dikesan:
                with open(FAIL_DATABASE_HASH, 'w') as f:
                    json.dump(database_semasa, f, indent=4)
            
            # Kemas kini memori data global untuk JavaScript Dashboard
            DATA_MATRIX_GLOBAL['soc'] = database_semasa

        except Exception as e:
            print("Error Sentinel Loop:", e)

# Hidupkan ejen pemantau keselamatan di belakang tab secara autopilot
threading.Thread(target=jalankan_integrity_sentinel, daemon=True).start()

# =====================================================================
# 🌐 STRUKTUR FRONTEND FLASK DASHBOARD (DARI SOURCE 2)
# =====================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DuoGuard Global Cyber Matrix</title>
    <style>
        body { background-color: #0d0d0d; color: #00ff00; font-family: 'Courier New', monospace; margin: 20px; }
        .container { max-width: 900px; margin: auto; border: 1px solid #00ff00; padding: 20px; box-shadow: 0 0 15px #00ff00; }
        h1, h2 { text-align: center; text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 5px #00ff00; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .card { border: 1px solid #00ff00; padding: 15px; background: #141414; }
        .status-ok { color: #00ff00; font-weight: bold; }
        .status-alert { color: #ff0000; font-weight: bold; text-shadow: 0 0 5px #ff0000; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #00ff00; padding: 8px; text-align: left; font-size: 12px; }
        th { background-color: #1a1a1a; }
        .footer { text-align: center; margin-top: 30px; font-size: 11px; color: #888; }
    </style>
    <script>
        setInterval(function() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('miner-status').innerText = data.miner_status;
                    document.getElementById('miner-status').className = "status-ok";
                    
                    let tableBody = document.getElementById('soc-table');
                    tableBody.innerHTML = '';
                    for (const [file, hash] of Object.entries(data.soc)) {
                        let shortHash = hash.substring(0, 25);
                        let statusFail = hash === "FILE_NOT_FOUND_YET" ? "<span class='status-alert'>[MISSING]</span>" : "<span class='status-ok'>[SECURE]</span>";
                        tableBody.innerHTML += `<tr><td>${file}</td><td><code>${shortHash}...</code></td><td>${statusFail}</td></tr>`;
                    }
                });
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <h1>⚡ DUOGUARD GLOBAL CLOUD MATRIX ⚡</h1>
        <p style="text-align:center; color:#888;">Pusat Kawalan Siber Menggunakan Cloud Hosting</p>
        
        <div class="grid">
            <div class="card">
                <h2>⛏️ Remote Miner</h2>
                <p>Algoritma: <span class="status-ok">RandomX (Monero)</span></p>
                <p>Status Enjin: <span id="miner-status" class="status-ok">RUNNING</span></p>
                <p>Target Pool: <span style="color: #ffff00;">pool.hashvault.pro</span></p>
            </div>
            
            <div class="card">
                <h2>🛡️ Sentinel Cloud Link</h2>
                <p>Modul: <span>File Integrity Embedded</span></p>
                <p>Status Gerbang: <span class="status-ok">MONITORING INTERNAL HOS</span></p>
                <p>Notifikasi: <span style="color: #00ffff;">Telegram Active</span></p>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <h2>📂 Fail Hos Render Dipantau Secara Tempatan (Live Cluster)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Nama Fail</th>
                        <th>Hash SHA-256 Semasa</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="soc-table">
                </tbody>
            </table>
        </div>

        <div class="footer">
            DuoGuard SOC v3.5 [Embedded Cloud Edition] - No External Post Agent Needed.
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(DATA_MATRIX_GLOBAL)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
