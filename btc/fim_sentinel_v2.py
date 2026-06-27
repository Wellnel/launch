import os
import hashlib
import time
import json
import requests

# Tetapan Warna Terminal
KUNING = "\033[93m"
HIJAU = "\033[92m"
MERAH = "\033[91m"
BIRU = "\033[94m"
RESET = "\033[0m"

# 📂 Fail Kritikal yang Diperhatikan oleh DuoGuard_SOC
FAIL_DILINDUNGI = {
    "config_json": "config.json",
    "miner_script": "miner_extreme_v2.py"
}
FAIL_DATABASE_HASH = "duoguard_hashes.json"

# 🤖 Masukkan API Token dari @BotFather & Chat ID dari @userinfobot bos di sini
TELEGRAM_TOKEN = "7964651809:AAFXMrLDM2d5A6hAYpsisIZguIDnJvvfFWU"
TELEGRAM_CHAT_ID = "6065278352"

def hantar_amaran_telegram(mesej):
    """Menembak notifikasi kecemasan terus ke Telegram bos"""
    if "MASUKKAN_TOKEN" in TELEGRAM_TOKEN:
        return # Abaikan jika belum setup token
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesej,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"{MERAH}[!] Gagal menghantar isyarat Telegram: {e}{RESET}")

def kira_sha256(jalan_fail):
    hashing = hashlib.sha256()
    try:
        with open(jalan_fail, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hashing.update(chunk)
        return hashing.hexdigest()
    except FileNotFoundError:
        return None

def bina_pangkalan_data_awal():
    database_hash = {}
    print(f"{BIRU}[+] Mengunci fail sistem ke dalam pangkalan data DuoGuard...{RESET}")
    
    for nama_label, jalan_fail in FAIL_DILINDUNGI.items():
        if os.path.exists(jalan_fail):
            hash_semasa = kira_sha256(jalan_fail)
            database_hash[jalan_fail] = hash_semasa
            print(f"🔒 {HIJAU}[DIKUNCI]{RESET} {jalan_fail} -> {hash_semasa[:15]}...")
            
    with open(FAIL_DATABASE_HASH, 'w') as f:
        json.dump(database_hash, f, indent=4)
    print(f"{HIJAU}[✓] Pangkalan data rujukan berjaya disimpan!{RESET}\n")
    return database_hash

def mula_pemantauan_soc(database_rujukan):
    print(f"{BIRU}[🚀] DuoGuard_SOC: Integrity Sentinel bersiap sedia. Memulakan rondaan...{RESET}")
    print(f"{KUNING}[+] Amaran Telegram diaktifkan. Tekan CTRL+C untuk berhenti.{RESET}\n")
    
    hantar_amaran_telegram("🚀 *DuoGuard SOC Alert*\n`Integrity Sentinel` berjaya dilancarkan. Semua fail sistem dipantau rapat!")
    
    while True:
        try:
            time.sleep(5) 
            
            # Kita tukar ke list(items()) supaya selamat untuk dipadam/dikemas kini secara dinamik
            for jalan_fail, hash_asal in list(database_rujukan.items()):
                if not os.path.exists(jalan_fail):
                    print(f"\n🚨 {MERAH}[BAHAYA]{RESET} Fail telah DIPADAMKAN: {jalan_fail}!")
                    hantar_amaran_telegram(f"🚨 *DUOGUARD SOC WARNING!*\n\nFail kritikal dipadamkan: `{jalan_fail}`")
                    del database_rujukan[jalan_fail]
                    with open(FAIL_DATABASE_HASH, 'w') as f:
                        json.dump(database_rujukan, f, indent=4)
                    continue
                
                hash_semasa = kira_sha256(jalan_fail)
                
                if hash_semasa != hash_asal:
                    print(f"\n🚨 {MERAH}[BAHAYA - DETECTED]{RESET} Modifikasi dikesan pada: {KUNING}{jalan_fail}{RESET}!")
                    print(f"   ↳ Hash Asal:    {HIJAU}{hash_asal[:15]}...{RESET}")
                    print(f"   ↳ Hash Baharu:  {MERAH}{hash_semasa[:15]}...{RESET}")
                    
                    msg = (
                        f"🚨 *DUOGUARD SOC WARNING!*\n\n"
                        f"Modifikasi dikesan pada fail sistem!\n"
                        f"📂 *Fail:* `{jalan_fail}`\n\n"
                        f"🔹 *Hash Asal:* `{hash_asal[:15]}...`\n"
                        f"🔺 *Hash Baharu:* `{hash_semasa[:15]}...`"
                    )
                    hantar_amaran_telegram(msg)
                    
                    # ✅ KEMAS KINI DATABASE AUTOMATIK (Selesai isu spam log)
                    database_rujukan[jalan_fail] = hash_semasa
                    with open(FAIL_DATABASE_HASH, 'w') as f:
                        json.dump(database_rujukan, f, indent=4)
                    print(f"{HIJAU}[✓] Pangkalan data dikemas kini dengan hash baharu. Loop ditenangkan.{RESET}")
                        
        except KeyboardInterrupt:
            print(f"\n{KUNING}[*] Integrity Sentinel ditutup secara bersih.{RESET}")
            hantar_amaran_telegram("⚠️ *DuoGuard SOC Alert*\n`Integrity Sentinel` ditutup secara manual.")
            break

if __name__ == "__main__":
    if not os.path.exists(FAIL_DATABASE_HASH):
        db_rujukan = bina_pangkalan_data_awal()
    else:
        print(f"{HIJAU}[✓] Pangkalan data rujukan sedia ada ditemui.{RESET}")
        with open(FAIL_DATABASE_HASH, 'r') as f:
            db_rujukan = json.load(f)
            
    mula_pemantauan_soc(db_rujukan)
