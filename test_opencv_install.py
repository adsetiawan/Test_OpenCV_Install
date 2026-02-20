import sys
from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_rgb(title: str, bgr_img: np.ndarray) -> None:
    """Convert BGR (OpenCV) -> RGB (matplotlib) and show."""
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    plt.figure()
    plt.title(title)
    plt.axis("off")
    plt.imshow(rgb)


def show_gray(title: str, gray_img: np.ndarray) -> None:
    plt.figure()
    plt.title(title)
    plt.axis("off")
    plt.imshow(gray_img, cmap="gray")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python test_opencv_install.py <path_gambar>")
        print("Contoh: python test_opencv_install.py data/contoh.jpg")
        return 2

    img_path = Path(sys.argv[1])
    if not img_path.exists():
        print(f"ERROR: file tidak ditemukan: {img_path}")
        return 2

    # 1) Load gambar
    img = cv2.imread(str(img_path))
    if img is None:
        print("ERROR: cv2.imread gagal. Pastikan format file gambar valid.")
        return 2

    print("OpenCV version:", cv2.__version__)
    print("Image shape (H, W, C):", img.shape)

    # 2) Resize (jaga rasio)
    target_w = 640
    h, w = img.shape[:2]
    scale = target_w / w if w > target_w else 1.0
    resized = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    # 3) Grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 4) Blur (reduksi noise)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 5) Edge detection (Canny)
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

    # 6) Buat overlay edges di atas gambar (visualisasi)
    overlay = resized.copy()
    overlay[edges > 0] = (0, 255, 0)  # edge jadi hijau

    # 7) Simpan hasil ke folder output
    out_dir = Path("output_test")
    out_dir.mkdir(exist_ok=True)

    cv2.imwrite(str(out_dir / "01_resized.jpg"), resized)
    cv2.imwrite(str(out_dir / "02_gray.jpg"), gray)
    cv2.imwrite(str(out_dir / "03_blurred.jpg"), blurred)
    cv2.imwrite(str(out_dir / "04_edges.jpg"), edges)
    cv2.imwrite(str(out_dir / "05_overlay_edges.jpg"), overlay)

    print(f"Hasil disimpan di folder: {out_dir.resolve()}")

    # 8) Tampilkan hasil (matplotlib)
    show_rgb("Original (resized)", resized)
    show_gray("Grayscale", gray)
    show_gray("Blurred", blurred)
    show_gray("Edges (Canny)", edges)
    show_rgb("Overlay edges (green)", overlay)

    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
