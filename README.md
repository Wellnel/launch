# ⚡ DuoGuard SOC & Mining Matrix v2.0 (2026) ⚡

Sistem integrasi gandingan pelombong kripto Monero (XMR) berprestasi tinggi bersama ejen kawalan integriti keselamatan siber peribadi (SOC) di persekitaran Android Termux.

---

## 📂 Struktur Direktori ~/launch

*   **`config.json`**: Fail konfigurasi XMRig yang dioptimumkan (4 Cores, TLS Enkripsi Port 443, Mod Latar Belakang).
*   **`duoguard_hashes.json`**: Pangkalan data rujukan SHA-256 untuk mengunci integriti fail kritikal.
*   **`fim_sentinel_v2.py`**: Skrip File Integrity Monitor yang meronda setiap 5 saat dan terhubung ke Telegram Bot.
*   **`dashboard.py`**: Pelayan web mini Flask untuk memaparkan grafik konsol bertema siber secara masa nyata.
*   **`cert.pem` & `cert_key.pem`**: Sijil keselamatan kriptografi TLS.
*   **`run.sh`**: Skrip pembuka/peluncur utama.

---

## 🚀 Cara Meluncurkan Sistem (Langkah demi Langkah)

Pastikan anda berada di dalam folder induk sebelum memulakan mana-mana modul:
```bash
cd ~/launch
