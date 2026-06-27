# DuoGuard_SOC 🛡️

DuoGuard_SOC adalah sistem pengurusan Pusat Operasi Keselamatan (SOC) mini berkuasa tinggi yang direka khas untuk memantau, mengesan, dan memberi amaran terhadap sebarang pencerobohan atau modifikasi fail kritikal pada pelayan secara masa nyata (Real-Time).

Sistem ini dilengkapi dengan modul **Integrity Sentinel**—sebuah sistem Pemantauan Integriti Fail (FIM) ringan yang memanfaatkan algoritma kriptografi SHA-256 untuk mengunci imej fail sistem dan menyepadukan amaran pintar terus ke Telegram API.

---

## ✨ Ciri-Ciri Utama
* **File Integrity Monitoring (FIM):** Mengunci acuan hash asal fail kritikal dan mengesan sebarang perubahan bit atau kandungan fail dalam masa 5 saat.
* **Anti-Log Flooding Engine:** Mengandungi mekanik pengemaskinian pangkalan data dinamik bagi mengelakkan lambakan log amaran berulang (*infinite loop spam*) dan mengekalkan kestabilan kuota API.
* **Telegram Incident Notification:** Menembak notifikasi amaran insiden keselamatan siber berserta pecahan forensik maklumat hash (Hash Asal vs Hash Baharu) terus ke peranti mudah alih pentadbir.
* **Kelebihan Pemrosesan Blok Memori:** Membaca fail dalam bentuk serpihan buffer kecil (4096 bytes) bagi mengelakkan serangan ranap memori (*system crash*) jika memantau fail berskala besar.

---

## 📂 Struktur Projek
```text
DuoGuard_SOC/
├── config.json            # Fail konfigurasi sistem & credential
├── duoguard_hashes.json   # Pangkalan data rujukan rupa bentuk hash (Baseline)
├── fim_sentinel_v2.py     # Skrip ejen utama ronda keselamatan (FIM)
└── README.md              # Dokumentasi projek

🚀 Panduan Pemasangan & Pengaktifan
​1. Keperluan Prasyarat
​Pastikan persekitaran peranti anda (Linux / Termux Android) telah dipasang dengan Python 3 dan pustaka requests.

pip install requests

2. Konfigurasi Ejen Bot Telegram
​Buka fail fim_sentinel_v2.py dan kemas kini pemanduan parameter API mengikut bot peribadi anda:

TELEGRAM_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

3. Melancarkan Enjin Rondaan
​Jalankan skrip utama untuk memulakan penguncian pangkalan data baseline dan pemantauan aktif:

python fim_sentinel_v2.py

📊 Contoh Log Paparan Insiden
​Log Terminal (Ejen Rondaan)
[✓] Pangkalan data rujukan sedia ada ditemui.
[🚀] DuoGuard_SOC: Integrity Sentinel bersiap sedia. Memulakan rondaan...
[+] Amaran Telegram diaktifkan. Tekan CTRL+C untuk berhenti.

🚨 [BAHAYA - DETECTED] Modifikasi dikesan pada: config.json!
   ↳ Hash Asal:    a1d7fa84b7b001d...
   ↳ Hash Baharu:  28b2340fbd88bf9...
[✓] Pangkalan data dikemas kini dengan hash baharu. Loop ditenangkan.

Amaran Pada Aplikasi Telegram

🚨 DUOGUARD SOC WARNING!

Modifikasi dikesan pada fail sistem!
📂 Fail: config.json

🔹 Hash Asal: a1d7fa84b7b001d...
🔺 Hash Baharu: 28b2340fbd88bf9...

🛡️ Pelan Pembangunan Masa Hadapan (Roadmap)
​[ ] Mod Pemulihan Kendiri (Self-Healing System): Mengembalikan fail asal secara automatik daripada direktori sandaran tersembunyi sekiranya modifikasi haram dikesan.
​[ ] Dynamic Directory Deep Scan: Keupayaan memantau keseluruhan direktori induk secara rekursif termasuk mengesan penambahan fail baharu yang tidak dikenali.
​[ ] SSH Honeypot Trap: Integrasi pemantauan log pencerobohan cubaan brute-force pelayan dan auto-ban IP penyerang menggunakan ip-routing.
​⭐ Dibangunkan oleh penggodam beretika untuk keselamatan persekitaran digital yang lebih utuh.



