# Pengujian Instalasi OpenCV

Python script ini dimaksudkan untuk melakukan pengujian instalasi OpenCV menggunakan Miniconda. Script ini merupakan bagian dari buku **Computer Vision dan Pengolahan Citra Digital Dengan OpenCV: Dari Dasar Hingga Lanjutan Disertai Studi Kasus**. 

# Menginstall Library dan Paket CV
Untuk melkakukan instalasi library dan paket pada environment di Miniconda dapat dilakukan dengan perintah berikut:

```bash
conda install -c conda-forge opencv numpy matplotlib pillow scikit-image jupyter imutils ffmpeg imageio
```

# Sintaks Pengujian

1) Tes instalasi tanpa gambar (pasti jalan)
2) Tes dengan gambar sendiri
3) Tes webcam (realtime 10 detik)
4) Mode “headless” (tanpa tampil) tapi tetap simpan output
5) Tidak mau simpan output
