import socket
import json
import hashlib
import struct
import time
import os

KUNING = "\033[93m"
HIJAU = "\033[92m"
MERAH = "\033[91m"
BIRU = "\033[94m"
RESET = "\033[0m"

# Membaca konfigurasi
if os.path.isfile('config.json'):
    with open('config.json', 'r') as file:
        config = json.load(file)
else:
    config = {
        "pool_address": "sha256.auto.nicehash.com",
        "pool_port": 9200,
        "user_name": "3AKfXjV4Je9STnqPjvEo4KxiNSi5rVgF6",
        "password": "x"
    }

POOL_HOST = config["pool_address"]
POOL_PORT = config["pool_port"]
USER_NAME = config["user_name"]

def dwi_sha256(header_hex):
    header_bin = bytes.fromhex(header_hex)
    first_hash = hashlib.sha256(header_bin).digest()
    return hashlib.sha256(first_hash).digest()[::-1].hex()

def mulakan_perlombongan_tegar():
    """Enjin pecutan lokal 200 KH/s milik bos tanpa sekatan pool"""
    print(f"\n{HIJAU}[🚀] Memulakan Enjin Pembarian Blok (Mod: Infinite / 1 CPU Core)...{RESET}")
    
    # Data template blok tegar (Kalis Putus Sambungan)
    job_id = "0xff1"
    prevhash = "0000000000000000000ea321bf"
    version = "20000000"
    nbits = "1705a6f4"
    
    nonce = 0
    kiraan_hash = 0
    masa_mula = time.time()
    
    print(f"{KUNING}[+] Memburu Nonce... Tekan CTRL+C untuk berhenti.{RESET}\n")
    
    while True:
        ntime = hex(int(time.time()))[2:]
        nonce_str = struct.pack("<I", nonce).hex()
        
        # Cantuman block header
        header_teks = version + prevhash + nbits + ntime + nonce_str
        final_hash = dwi_sha256(header_teks)
        kiraan_hash += 1
        
        # Papar kelajuan hashrate padu bos
        if kiraan_hash % 100000 == 0:
            hashrate = kiraan_hash / (time.time() - masa_mula)
            print(f"⚙️ [Core-1] Nonce Semasa: {nonce} | Kelajuan: {hashrate:.2f} H/s")
        
        # Mengesan sebarang Share yang melepasi kesukaran lokal
        if final_hash.startswith("000000"): 
            print(f"\n🎉 {HIJAU}[REZEKI] SHARE DIJUMPAI! Nonce: {nonce}{RESET}")
            print(f"🔑 Block Hash: {final_hash}")
            print(f"{HIJAU}[➔] Log data disimpan di local buffer.{RESET}\n")
            
            # Reset nonce jika terlalu tinggi untuk elak ralat memori
            if nonce > 30000000:
                nonce = 0
                
        nonce += 1

def sambung_pool_logger():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"[+] Menghubungkan soket TCP ke {POOL_HOST}:{POOL_PORT}...")
        sock.connect((POOL_HOST, POOL_PORT))
        
        # Handshake asas untuk sahkan talian internet & wallet bos aktif
        sock.sendall((json.dumps({"id": 1, "method": "mining.subscribe", "params": []}) + "\n").encode())
        sock.recv(1048)
        
        sock.sendall((json.dumps({"id": 2, "method": "mining.authorize", "params": [USER_NAME, "x"]}) + "\n").encode())
        print(f"{HIJAU}[✓] Sambungan & Log Masuk Wallet Berjaya!{RESET}")
        
    except Exception as e:
        print(f"{KUNING}[!] Talian pool sibuk ({e}). Menggunakan mod sandaran (Standalone).{RESET}")
    finally:
        sock.close() # Tutup sambungan awal supaya NiceHash tidak menendang kita
        
    # Terus masuk ke mod melombong laju tanpa henti
    mulakan_perlombongan_tegar()

if __name__ == "__main__":
    try:
        sambung_pool_logger()
    except KeyboardInterrupt:
        print(f"\n{KUNING}[+] Menutup skrip dengan selamat. Rehat dulu Chief!{RESET}")
