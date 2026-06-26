from flask import Flask, render_template_string, jsonify, request
import os

app = Flask(__name__)

# Pembolehubah global untuk menyimpan data sementara dalam memori server
DATA_MATRIX_GLOBAL = {
    "soc": {},
    "miner_status": "OFFLINE",
    "hashrate_sekarang": "0 H/s"
}

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
        // Auto-refresh halaman setiap 3 saat untuk menarik data live dari API awan
        setInterval(function() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('miner-status').innerText = data.miner_status;
                    if(data.miner_status === "RUNNING") {
                        document.getElementById('miner-status').className = "status-ok";
                    } else {
                        document.getElementById('miner-status').className = "status-alert";
                    }
                    
                    let tableBody = document.getElementById('soc-table');
                    tableBody.innerHTML = '';
                    for (const [file, hash] of Object.entries(data.soc)) {
                        tableBody.innerHTML += `<tr><td>${file}</td><td><code>${hash.substring(0, 30)}...</code></td><td class="status-ok">[SECURE]</td></tr>`;
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
                <p>Status Enjin: <span id="miner-status" class="status-alert">WAITING PING...</span></p>
                <p>Target Pool: <span style="color: #ffff00;">pool.hashvault.pro</span></p>
            </div>
            
            <div class="card">
                <h2>🛡️ Sentinel Cloud Link</h2>
                <p>Modul: <span>File Integrity Sync</span></p>
                <p>Status Gerbang: <span class="status-ok">MENUNGGU DATA API</span></p>
                <p>Notifikasi: <span style="color: #00ffff;">Telegram Active</span></p>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <h2>📂 Fail Sistem Dipantau Dari Jauh (Live Node)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Nama Fail</th>
                        <th>Hash SHA-256 Semasa</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="soc-table">
                    <!-- Data akan dimasukkan secara dinamik oleh JavaScript -->
                </tbody>
            </table>
        </div>

        <div class="footer">
            DuoGuard SOC v3.0 [Cloud Edition] - Monitoring from Anywhere.
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# API Endpoint untuk pelayar web membaca data
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(DATA_MATRIX_GLOBAL)

# API Endpoint BAHARU untuk menerima data POST daripada Termux telefon bos
@app.route('/api/update', methods=['POST'])
def update_status():
    data_terima = request.json
    if data_terima:
        DATA_MATRIX_GLOBAL['soc'] = data_terima.get('soc', {})
        DATA_MATRIX_GLOBAL['miner_status'] = data_terima.get('miner_status', 'RUNNING')
        return jsonify({"status": "SUCCESS", "message": "Data berjaya dikemas kini di awan!"}), 200
    return jsonify({"status": "ERROR", "message": "Tiada data dikesan"}), 400

if __name__ == '__main__':
    # Server akan mendengar di port 5000 (Sesuai untuk lokal & cloud)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
