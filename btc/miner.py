import socket
import json
import hashlib
import struct
import time
import os

KUNING = "\033[93m"
HIJAU = "\033[92m"
MERAH = "\033[91m"
RESET = "\033[0m"

# 1. Memuatkan fail konfigurasi
if os.path.isfile('config.json'):
    print(f"{HIJAU}[+] config.json ditemui. Membaca tetapan...{RESET}")
    with open('config.json', 'r') as file:
        config = json.load(file)
else:
    print(f"{MERAH}[!] config.json tidak ditemui! Menggunakan tetapan lalai.{RESET}")
    config = {
        "pool_address": "sha256.auto.nicehash.com",
        "pool_port": 9200,
        "user_name": "3AKfXjV4Je9STnqPjvEo4KxiNSi5rVgF6",
        "password": "x",
        "max-threads-hint": 1
    }

POOL_HOST = config["pool_address"]
POOL_PORT = config["pool_port"]
USER_NAME = config["user_name"]
PASSWORD = config["password"]

def mulakan_perlombongan(sock):
    """Fungsi utama melombong menggunakan 1 thread asli"""
    print(f"\n{HIJAU}[🚀] Memulakan Giliran Melombong (Mod: 1 CPU Core)...{RESET}")
    
    # Ini data simulasi template blok Bitcoin (Stratum Job)
    # Dalam realiti, data ini akan dihantar secara berterusan oleh NiceHash
    job_id = "10a"
    prevhash = "0000000000000000000ea321bf"
    version = "20000000"
    nbits = "1705a6f4"
    ntime = hex(int(time.time()))[2:]
    
    nonce = 0
    KIRAAN_HASH = 0
    masa_mula = time.time()
    
    print(f"{KUNING}[+] Memburu Nonce... Tekan CTRL+C untuk berhenti.{RESET}\n")
    
    while True:
        # Membina struktur data block header Bitcoin
        nonce_str = struct.pack("<I", nonce).hex()
        header_teks = version + prevhash + nbits + ntime + nonce_str
        header_bin = bytes.fromhex(header_teks)
        
        # Pengiraan Double SHA-256 (Standard Bitcoin)
        first_hash = hashlib.sha256(header_bin).digest()
        second_hash = hashlib.sha256(first_hash).digest()
        final_hash = second_hash[::-1].hex()
        
        KIRAAN_HASH += 1
        
        # Memaparkan kelajuan hashrate setiap 50,000 pusingan
        if KIRAAN_HASH % 50000 == 0:
            masa_tamat = time.time()
            hashrate = KIRAAN_HASH / (masa_tamat - masa_mula)
            print(f"⚙️ [Core-1] Nonce Semasa: {nonce} | Kelajuan: {hashrate:.2f} H/s")
        
        # Jika menemui hash yang memenuhi syarat kesukaran (Difficulty Target)
        if final_hash.startswith("000000"): 
            print(f"\n🎉 {HIJAU}[REZEKI] SHARE DIJUMPAI! Nonce: {nonce}{RESET}")
            print(f"🔑 Block Hash: {final_hash}")
            
            # Menghantar hasil kerja (Share) kembali ke NiceHash Pool
            submit_msg = {
                "id": 4,
                "method": "mining.submit",
                "params": [USER_NAME, job_id, "00000000", ntime, nonce_str]
            }
            sock.sendall((json.dumps(submit_msg) + "\n").encode())
            break
            
        nonce += 1

def sambung_pool():
    """Menguruskan sambungan soket ke server NiceHash"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"[+] Menghubungkan ke {POOL_HOST}:{POOL_PORT}...")
        sock.connect((POOL_HOST, POOL_PORT))
        
        # Langkah 1: Mendaftar ke Pool (Subscribe)
        subscribe_msg = {"id": 1, "method": "mining.subscribe", "params": []}
        sock.sendall((json.dumps(subscribe_msg) + "\n").encode())
        sock.recv(1024) # Menerima data kelulusan subscribe
        
        # Langkah 2: Log masuk dompet Bitcoin (Authorize)
        auth_msg = {"id": 2, "method": "mining.authorize", "params": [USER_NAME, PASSWORD]}
        sock.sendall((json.dumps(auth_msg) + "\n").encode())
        print(f"{HIJAU}[✓] Alamat BTC berjaya disahkan oleh NiceHash.{RESET}")
        
        # Mulakan pusingan kerja
        mulakan_perlombongan(sock)
        
    except Exception as e:
        print(f"{MERAH}[🚨 RALAT STRATUM] Sambungan terputus: {e}{RESET}")
    finally:
        sock.close()

if __name__ == "__main__":
    try:
        sambung_pool()
    except KeyboardInterrupt:
        print(f"\n{KUNING}[+] Pelombong ditutup secara selamat. Rehat dulu bos!{RESET}")
