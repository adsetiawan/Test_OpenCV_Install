# Pengujian Instalasi OpenCV

Python script ini dimaksudkan untuk melakukan pengujian instalasi OpenCV menggunakan Miniconda. Script ini merupakan bagian dari buku **Computer Vision dan Pengolahan Citra Digital Dengan OpenCV: Dari Dasar Hingga Lanjutan Disertai Studi Kasus**. 

# Menginstall Library dan Paket CV
Untuk melkakukan instalasi library dan paket pada environment di Miniconda dapat dilakukan dengan perintah berikut:

```bash
conda install -c conda-forge opencv numpy matplotlib pillow scikit-image jupyter imutils ffmpeg imageio
```

# Sintaks Pengujian
Pengujian dapat dilakukan menggunakan script test_opencv_install.py dengan perintah sebagai berikut:

```bash
python test_opencv_install.py nama_citra
```

Contoh

```bash
python test_opencv_install.py lenna.png
```
Pengujian webcam dapat menggunakan test_webcam.py

```bash
python test_webcam.py
```
Pengujian yang paling lengkap dapat menggunakan opencv_install_test.py. Berikut ini adalah sintaks untuk menjalankan pengujian menggunakan script ini.

## Tes instalasi tanpa gambar (pasti jalan)

```bash
python opencv_install_test.py --show
```

## Tes dengan gambar sendiri

```bash
python opencv_install_test.py contoh.jpg --show
```

## Tes webcam (realtime 10 detik)

```bash
python opencv_install_test.py --webcam --show
```

Jika kamera tidak terbuka silakan dicoba perintah berikut:

```bash
python opencv_install_test.py --webcam --show --cam-index 1
```
Beberapa laptop memiliki:
- kamera internal = index 0
- kamera virtual = index 1
- kamera USB = index 2

## Mode “headless” (tanpa tampil) tapi tetap simpan output

```bash
python opencv_install_test.py
python opencv_install_test.py --webcam --duration 5
```

## Tidak mau simpan output

```bash
python opencv_install_test.py --show --no-save
```
