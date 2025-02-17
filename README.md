# python_netcat

 adalah sebuah aplikasi sederhana yang memungkinkan eksekusi perintah jarak jauh antara client dan server menggunakan socket. Program ini mendukung perintah dasar seperti `cd` untuk mengganti direktori, serta menjalankan perintah lainnya di server yang terhubung.

## Fitur Utama

- Eksekusi perintah jarak jauh menggunakan koneksi TCP.
- Mendukung perintah shell seperti `ls`, `pwd`, dan lainnya.
- Mendukung perintah `cd` untuk berpindah direktori di server.
- Mode server dan client terpisah.
- Menampilkan prompt yang memperlihatkan direktori kerja saat ini.

## Persyaratan

- Python 3.x
- Paket Python standar (`socket`, `subprocess`, `threading`, `os`, dll)

## Cara Penggunaan

### 1. Menjalankan Server

Untuk menjalankan aplikasi sebagai **server**, buka terminal dan jalankan perintah berikut:

```bash
python script.py -m server -t 0.0.0.0 -p 5555
```
`-m server` : Menjalankan server mode.  
`-t` : Alamat IP yang akan digunakan oleh server untuk mendengarkan koneksi (default: `0.0.0.0`, menerima koneksi dari semua IP).  
`-p` : Port yang digunakan oleh server untuk mendengarkan koneksi (default: `5555`).  
server akan menunggu koneksi client

### 2. Menjalankan Client

Untuk menjalankan aplikasi sebagai **client**, buka terminal dan jalankan perintah berikut:

```bash
python script.py -m client -t <IP_SERVER> -p 5555
```
`-m client` : Menjalankan client mode.
`-t` : IP dari server yang ingin dihubungi.
`-p` : Port server yang ingin dihubungi.  
Setelah terhubung, kamu dapat mulai mengirimkan perintah yang ingin dijalankan di server.

### 3. Perintah yang Didukung

`cd <direktori>` : Mengubah direktori kerja di server.
Perintah shell lainnya seperti `ls`, `pwd`, `cat`, dll, untuk menjalankan perintah di server.
`exit` : Menutup koneksi client ke server.

### Kelebihan

Mudah digunakan: Program ini menyediakan antarmuka yang sederhana dan mudah dimengerti untuk komunikasi antara client dan server.
Dukungan perintah shell: Selain perintah dasar, dapat mengeksekusi perintah shell biasa seperti `ls`, `cat`, `pwd`, dll.
Mendukung perubahan direktori: Pengguna dapat menggunakan perintah `cd` untuk berpindah direktori di server, menjadikannya lebih fleksibel dalam penggunaan.
Multi-threading: Server dapat menangani beberapa koneksi client secara bersamaan menggunakan threading.

### Kekurangan

Keamanan terbatas: Skrip ini tidak melakukan verifikasi atau perlindungan terhadap perintah yang diterima. Penggunaan di lingkungan yang tidak aman bisa berisiko.
Fitur terbatas: Skrip ini hanya mendukung perintah dasar dan tidak mendukung banyak fitur lain seperti autentikasi atau enkripsi.
Tidak ada handling timeout: Koneksi client dan server tidak memiliki mekanisme timeout yang memadai jika koneksi terputus atau terlalu lama.
Tidak ada logging: Tidak ada logging atau pencatatan aktivitas yang dilakukan pada server.

### Lisensi

Proyek ini dilisensikan di bawah MIT License.