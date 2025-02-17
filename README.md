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