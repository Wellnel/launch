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

# 📂 Semua fail penting dalam folder ~/launch yang dikawal ketat
FAIL_DILINDUNGI = {
    "config.json": "config.json",
    "cert_key.pem": "cert_key.pem",
    "cert.pem": "cert.pem",
    "fim_sentinel_v2.py": "fim_sentinel_v2.py",
    "README.md": "README.md",
    "run.sh": "run.sh"
}
FAIL_DATABASE_HASH = "duoguard_hashes.json"

# 🤖 Maklumat Bot Telegram Peribadi Bos
TELEGRAM_TOKEN = "7964651809:AAFXMrLDM2d5A6hAYpsisIZguIDnJvvfFWU" # Sila masukkan token penuh @BotFather bos di sini
TELEGRAM_CHAT_ID = "6065278352" # Masukkan Chat ID bos

def hantar_amaran_telegram(mesej):
    """Menembak notifikasi kecemasan terus ke Telegram bos"""
    if "AA..." in TELEGRAM_TOKEN or not TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesej, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"{MERAH}[!] Gagal menghantar isyarat Telegram: {e}{RESET}")

def kira_sha256(jalan_fail):
    """Mengira cop jari digital SHA-256 bagi fail"""
    hashing = hashlib.sha256()
    try:
        with open(jalan_fail, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hashing.update(chunk)
        return hashing.hexdigest()
    except FileNotFoundError:
        return None

def selaras_dan_bina_baseline():
    """Membaca duoguard_hashes.json dan mengemas kini mana-mana hash placeholder"""
    database_hash = {}
    
    # Baca fail sedia ada jika wujud
    if os.path.exists(FAIL_DATABASE_HASH):
        try:
            with open(FAIL_DATABASE_HASH, 'r') as f:
                database_hash = json.load(f)
        except:
            database_hash = {}

    print(f"{BIRU}[+] Mengesahkan integrity baseline dalam folder ~/launch...{RESET}")
    kemas_kini_diperlukan = False

    for label_fail, jalan_fail in FAIL_DILINDUNGI.items():
        if os.path.exists(jalan_fail):
            hash_semasa = kira_sha256(jalan_fail)
            
            # Jika fail belum ada dalam JSON, atau masih bernilai placeholder, kita kemas kini nilai tulen
            if jalan_fail not in database_hash or "INITIAL_BASELINE_" in str(database_hash[jalan_fail]):
                database_hash[jalan_fail] = hash_semasa
                kemas_kini_diperlukan = True
                print(f"🔒 {HIJAU}[BASELINE BARU KUNCI]{RESET} {jalan_fail} -> {hash_semasa[:15]}...")
            else:
                print(f"🔒 {BIRU}[SEDIA ADA KEKAL]{RESET} {jalan_fail} -> {database_hash[jalan_fail][:15]}...")
        else:
            print(f"⚠️ {KUNING}[AMARAN]{RESET} Fail {jalan_fail} tiada di direktori. Melompati...")

    if kemas_kini_diperlukan:
        with open(FAIL_DATABASE_HASH, 'w') as f:
            json.dump(database_hash, f, indent=4)
        print(f"{HIJAU}[✓] Pangkalan data duoguard_hashes.json berjaya diselaraskan!{RESET}\n")
    else:
        print(f"{HIJAU}[✓] Pangkalan data rujukan sepadan sepenuhnya.{RESET}\n")
        
    return database_hash

def mula_pemantauan_soc(database_rujukan):
    print(f"{BIRU}[🚀] DuoGuard_SOC: Integrity Sentinel bersiap sedia di folder ~/launch.{RESET}")
    print(f"{KUNING}[+] Rondaan aktif setiap 5 saat. Tekan CTRL+C untuk berhenti.{RESET}\n")
    
    hantar_amaran_telegram("🚀 *DuoGuard SOC Alert*\n`Integrity Sentinel` berjaya dilancarkan di direktori induk `~/launch`!")
    
    while True:
        try:
            time.sleep(5)
            
            for jalan_fail, hash_asal in list(database_rujukan.items()):
                if not os.path.exists(jalan_fail):
                    print(f"\n🚨 {MERAH}[BAHAYA]{RESET} Fail dipadamkan secara haram: {jalan_fail}!")
                    hantar_amaran_telegram(f"🚨 *DUOGUARD SOC WARNING!*\n\nFail kritikal telah *DIPADAMKAN*:\n📂 `{jalan_fail}`")
                    del database_rujukan[jalan_fail]
                    with open(FAIL_DATABASE_HASH, 'w') as f:
                        json.dump(database_rujukan, f, indent=4)
                    continue
                
                hash_semasa = kira_sha256(jalan_fail)
                
                if hash_semasa != hash_asal:
                    print(f"\n🚨 {MERAH}[BAHAYA - DETECTED]{RESET} Modifikasi dikesan pada: {KUNING}{jalan_fail}{RESET}!")
                    
                    msg = (
                        f"🚨 *DUOGUARD SOC WARNING!*\n\n"
                        f"Modifikasi dikesan pada folder induk!\n"
                        f"📂 *Fail:* `{jalan_fail}`\n\n"
                        f"🔹 *Hash Asal:* `{hash_asal[:15]}...`\n"
                        f"🔺 *Hash Baharu:* `{hash_semasa[:15]}...`"
                    )
                    hantar_amaran_telegram(msg)
                    
                    # Kemas kini pangkalan data serta-merta untuk menenangkan loop spam
                    database_rujukan[jalan_fail] = hash_semasa
                    with open(FAIL_DATABASE_HASH, 'w') as f:
                        json.dump(database_rujukan, f, indent=4)
                    print(f"{HIJAU}[✓] Pangkalan data dikemas kini. Loop ditenangkan.{RESET}")
                    
        except KeyboardInterrupt:
            print(f"\n{KUNING}[*] Integrity Sentinel dihentikan bersih.{RESET}")
            break

if __name__ == "__main__":
    db_rujukan = selaras_dan_bina_baseline()
    mula_pemantauan_soc(db_rujukan)
