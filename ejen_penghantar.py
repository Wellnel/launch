import time
import json
import os
import requests

# Buat masa ini kita uji secara lokal dahulu (127.0.0.1)
# Nanti bila sudah host di Render, tukar URL ini ke pautan Render bos!
URL_SERVER_AWAN = "https://duoguard-matrix.onrender.com/api/update"
def ambil_data_lokal():
    if os.path.exists("duoguard_hashes.json"):
        try:
            with open("duoguard_hashes.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

print("🚀 Ejen Penghantar DuoGuard Global Aktif...")
print("Mengirim isyarat integriti ke dashboard...")

while True:
    try:
        data_hashes = ambil_data_lokal()
        
        # Pakejkan data untuk dihantar melalui internet
        payload = {
            "soc": data_hashes,
            "miner_status": "RUNNING"
        }
        
        # Hantar data menggunakan kaedah HTTP POST
        respon = requests.post(URL_SERVER_AWAN, json=payload, timeout=5)
        
        if respon.status_code == 200:
            print("[✓] Isyarat segerak (Sync) berjaya dihantar ke server!")
        else:
            print(f"[X] Gagal hantar. Respons server: {respon.status_code}")
            
    except Exception as e:
        print(f"[🚨] Ralat sambungan ke pelayan web: {e}")
        
    # Hantar data setiap 60 saat
    time.sleep(60)
