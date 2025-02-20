# Python NetCat - Remote Command Executor

## 🚀 Fitur
- Menjalankan perintah shell jarak jauh
- Bisa berpindah direktori dengan perintah `cd`
- Tidak ada duplikasi output atau baris kosong saat menekan enter
- Mendukung banyak koneksi client dengan multi-threading
- Mudah digunakan untuk keperluan administrasi jaringan

## 📌 Instalasi
Pastikan Python sudah terinstal, lalu clone repository ini:
```bash
git clone https://github.com/MeTakoyaki/python-netcat.git
cd python-netcat
```

Install dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

## 🔧 Cara Penggunaan

### **Menjalankan sebagai Server (Listener)**
```bash
python netcat.py -t x.x.x.x -p xxxx -l
```
👉 Server akan menunggu koneksi pada ip x.x.x.x port xxxx.

### **Menjalankan sebagai Client**
```bash
python netcat.py -t x.x.x.x -p xxxx
```
👉 Client akan terhubung ke server dan bisa menjalankan perintah shell.

### **Menjalankan Perintah**
Setelah client terhubung, ketik perintah seperti:
```bash
ls
pwd
cd /home/user
cat file.txt
```
Hasilnya akan dikirim kembali ke client.

### **Keluar dari Session**
Untuk keluar, cukup ketik:
```bash
exit
```

## ✅ Kelebihan
- **Mudah digunakan** dengan parameter `-l` untuk server dan tanpa `-l` untuk client
- **Lebih cepat dan stabil** dibandingkan NetCat tradisional
- **Bisa berpindah direktori (`cd`) tanpa masalah**
- **Dukungan multi-threading untuk banyak koneksi client**

## ❌ Kekurangan
- Tidak mendukung koneksi terenkripsi (sebaiknya gunakan dalam jaringan yang aman)
- Tidak memiliki autentikasi pengguna (bisa ditambahkan jika diperlukan)

## 📜 Lisensi
Proyek ini menggunakan lisensi **MIT**, yang berarti Anda bebas menggunakannya dengan syarat tetap mencantumkan atribusi kepada pembuatnya.

## 🤝 Kontribusi
Pull request sangat diterima! Silakan buat issue jika ada bug atau fitur yang ingin ditambahkan.

## 📞 Kontak
Jika ada pertanyaan, hubungi saya di [botnet.inbox@gmail.com](mailto:botnet.inbox@gmail.com).

---
✨ **Happy Hacking!** ✨

