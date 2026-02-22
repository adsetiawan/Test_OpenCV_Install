# Pengujian Instalasi OpenCV

Python script ini dimaksudkan untuk melakukan pengujian instalasi OpenCV menggunakan Miniconda. Script ini merupakan bagian dari buku **Computer Vision dan Pengolahan Citra Digital Dengan OpenCV: Dari Dasar Hingga Lanjutan Disertai Studi Kasus**. Sering kali saat instalasi library dan paket untuk CV ada beberapa hal yang tidak berjalan dengan baik. Oleh sebab itu saya menulis script yang memungkinkan pengujian instalasi tersebut. Pengujian ini dimaksudkan untuk memastikan OpenCV + NumPy + Matplotlib dapat berfungsi dengan baik.

## Menginstall Library dan Paket CV
Untuk melkakukan instalasi library dan paket pada environment di Miniconda dapat dilakukan dengan perintah berikut:

```bash
conda create --name cvclass python=3.11
conda install -c conda-forge opencv numpy matplotlib pillow scikit-image jupyter imutils ffmpeg imageio
```
Instalasi dapat juga menggunakan file environment.yml:

```yaml
name: cvclass
channels:
  - conda-forge
dependencies:
  - python=3.11
  - opencv
  - numpy
  - matplotlib
  - pillow
  - scikit-image
  - jupyter
  - imutils
  - ffmpeg
  - imageio
```
Untuk instalasi menggunakan yaml dapat menggunakan perintah berikut ini:

```bash
conda env create -f environment.yml
conda activate cvclass
```

## Pengujian Dasar
### Penampilan dan Pemrosesan Citra Dasar Menampilkan Citra dan Pemrosesan
Pengujian dapat dilakukan menggunakan script test_opencv_install.py dengan perintah sebagai berikut:

```bash
python test_opencv_install.py nama_citra
```
 
Contoh

```bash
python test_opencv_install.py lenna.png
```
### Pengujian webcam
Pengujian fungsi webcam menjadi penting untuk aplikasi-aplikasi Computer Vision. Pengujian webcam dapat menggunakan test_webcam.py. Fungsi dari program ini adalah: buka kamera, kemudian tampilkan grayscale + edges realtime.

```bash
python test_webcam.py
```
## Pengujian Lanjut
Pengujian yang paling lengkap dapat menggunakan opencv_install_test.py. Berikut ini adalah sintaks untuk menjalankan pengujian menggunakan script ini. Script ini mendukung opsi-opsi berikut ini:
- --show → tampilkan hasil (matplotlib untuk gambar; cv2.imshow untuk webcam)
- --webcam → uji webcam realtime
- --cam-index N → pilih index kamera (0/1/2…)
- --outdir → folder output
- --no-save → tidak menyimpan file hasil
- Tetap bisa jalan tanpa input gambar (auto-generate gambar sintetis)

### Tes instalasi tanpa gambar (pasti jalan)
Sintaks ini dimaksudkan untuk menguji hasil instalasi tanpa menggunakan citra. Citra sintetis akan ditampilkan untuk menggantikan citra yang sesungguhnya. Citra sintetis akan diproses menjadi citra grayscale, lalu diproses menggunakan morphology, blurred (gaussian), threshold, edge detection, dan overlay edges. Kemudian citra hasil proses disimpan di folder output_test/. Sintaksnya adalah sebagai berikut:

```bash
python opencv_install_test.py --show
```

### Tes dengan gambar sendiri
Pengujian ini menggunakan citra yang disediakan. Pengujian ini akan menampilkan citra asli dan citra hasil pemrosesan berupa citra grayscale, morphology, blurred (gaussian), threshold, edge detection, dan overlay edges.

```bash
python opencv_install_test.py contoh.jpg --show
```

### Tes webcam (realtime 10 detik)
Pengujian ini akan menampilkan 4 buah jendela webcam selama 10 detik (waktu default): input, gray, edge, dan everlay

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

### Mode “headless” (tanpa tampil) tapi tetap simpan output
Perintah yang dapat diberikan adalah sebagai berikut:
```bash
python opencv_install_test.py
python opencv_install_test.py --webcam --duration 5
```
Perintah pertama melakukan pemrosesan citra sintetis tanpa menampilkan jendela hasil proses, tapi file sintesis yang diproses akan disimpan pada frolder output_test/. Perintah kedua juga sama, yaitu membuka webcam ranpa menampilkan jendela tangkapan webcam dengan durasi 5 detik dan hasil proses disimpan di folder yang sama.

### Tidak mau simpan output
Perintah berikut ini menampilkan citra sintetis tanpa harus menyimpan hasil prosesnya.
```bash
python opencv_install_test.py --show --no-save
```
