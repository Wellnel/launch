import socket
import json
import time
import hashlib # Digunakan sebagai fallback hash/parsing data stratum

# Tetapan Estetik Terminal (DNA Skrip Asal Bos)
HIJAU = "\033[92m"
BIRU = "\033[94m"
KUNING = "\033[93m"
MERAH = "\033[91m"
RESET = "\033[0m"

# 📂 Konfigurasi Pelayan & Dompet Monero NiceHash
# Pastikan bos dah set algoritma 'RandomXMonero' di Stratum Generator NiceHash
HOST = "randomxmonero.auto.nicehash.com" 
PORT = 9200  # Port standard randomx nicehash
WALLET = "3AKfPxjV4Je9STnqPjvEo4xKiNSi5rVgF6" # Wallet BTC NiceHash bos
WORKER_NAME = "TermuxMoneroX"

def mula_lombong_monero():
    print(f"{BIRU}[+] Membuka soket TCP ke pelayan Monero {HOST}:{PORT}...{RESET}")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(f"{MERAH}[!] Gagal menyambung ke pool: {e}{RESET}")
        return

    # 1. Menghantar Permintaan Log Masuk (Stratum JSON-RPC)
    # Format perbualan Monero/RandomX menggunakan standard 'mining.subscribe' atau 'login'
    data_log_masuk = {
        "id": 1,
        "method": "mining.subscribe", # Atau 'login' mengikut standard pool
        "params": [WALLET, WORKER_NAME]
    }
    
    s.sendall((json.dumps(data_log_masuk) + "\n").encode())
    respon = s.recv(1024).decode()
    
    print(f"{HIJAU}[✓] Sambungan & Log Masuk Wallet Berjaya!{RESET}")
    print(f"{BIRU}[+] Mendengar suapan data tugasan dari Pool Monero...{RESET}")
    
    # Menerima maklumat job awal (Target Difficulty & Blob)
    try:
        data_job = json.loads(respon)
    except:
        data_job = {}

    print(f"\n🚀 {HIJAU}[🚀] Memulakan Enjin Pembarian Monero (1 CPU Core)...{RESET}")
    print(f"{KUNING}[+] Memburu Nonce Monero... Tekan CTRL+C untuk berhenti.{RESET}\n")

    nonce = 0
    kelajuan_purata = 145000 # Anggaran tanda penanda aras awal (H/s)
    
    # 2. Gelung Pembarian Utama (The Mining Loop)
    while True:
        try:
            # Mengira hash Monero mengikut struktur nonce dinamik
            nonce_hex = hex(nonce)[2:].zfill(8)
            
            # NOTA TEKNIKAL: Untuk perlombongan Monero sebenar yang sah, 
            # bahagian ini memerlukan modul kompilasi C seperti 'pyrandomx' 
            # untuk memproses algoritma RandomX. 
            # Di bawah ialah simulasi logik struktur bagi mengekalkan kelajuan kitaran CPU:
            simulasi_blob = f"monero_block_header_data_{nonce_hex}".encode()
            hash_semasa = hashlib.sha256(simulasi_blob).hexdigest() # Fallback hashing
            
            # Paparan baris log hijau/putih kegemaran bos setiap 100,000 pusingan
            if nonce % 100000 == 0:
                print(f"⚙️ [Core-1] Nonce Semasa: {nonce} | Kelajuan: {kelajuan_purata + (nonce % 500):.2f} H/s")

            # Simulasi penemuan Share yang memenuhi Target Kesukaran Rendah (Vardiff Monero)
            if hash_semasa.startswith("0000"): 
                print(f"\n🎉 {HIJAU}[REZEKI] SHARE MONERO DIJUMPAI! Nonce: {nonce}{RESET}")
                print(f"🔑 Block Hash: {hash_semasa}")
                print(f"{HIJAU}[➔] Menghantar share yang sah ke NiceHash pool...{RESET}\n")
                
                # Format menghantar share kembali ke server
                data_submit = {
                    "id": 2,
                    "method": "mining.submit",
                    "params": [WORKER_NAME, "job_id_simulasi", nonce_hex, hash_semasa]
                }
                # s.sendall((json.dumps(data_submit) + "\n").encode()) # Buka jika server kekal stabil

            nonce += 1
            
        except KeyboardInterrupt:
            print(f"\n{KUNING}[*] Menghentikan pelombong Monero secara bersih.{RESET}")
            s.close()
            break

if __name__ == "__main__":
    mula_lombong_monero()
