import argparse
from pathlib import Path
import sys
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def generate_synthetic_image(width: int = 960, height: int = 540) -> np.ndarray:
    """Buat gambar sintetis untuk testing (gradient + shape + text + noise)."""
    x = np.linspace(0, 255, width, dtype=np.uint8)
    grad = np.tile(x, (height, 1))

    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :, 0] = grad
    img[:, :, 1] = np.flipud(grad)
    img[:, :, 2] = 255 - grad

    cv2.rectangle(img, (50, 50), (350, 250), (255, 255, 255), 3)
    cv2.circle(img, (650, 180), 90, (0, 255, 255), 4)
    cv2.line(img, (50, 450), (900, 450), (255, 255, 255), 2)

    cv2.putText(
        img,
        "OpenCV Install Test",
        (60, 330),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    noise = np.random.normal(0.0, 10.0, size=img.shape).astype(np.int16)
    noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return noisy


def safe_imread(path: Path) -> np.ndarray | None:
    img = cv2.imread(str(path))
    return img


def process_image(img_bgr: np.ndarray) -> dict[str, np.ndarray]:
    """Pipeline sederhana untuk uji instalasi."""
    # Resize (maks width 800)
    h, w = img_bgr.shape[:2]
    target_w = 800
    scale = target_w / w if w > target_w else 1.0
    resized = cv2.resize(img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold Otsu
    _, th = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morfologi open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)

    # Edge Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Overlay edges (hijau)
    overlay = resized.copy()
    overlay[edges > 0] = (0, 255, 0)

    return {
        "00_input_resized": resized,
        "01_gray": gray,
        "02_blurred": blurred,
        "03_threshold_otsu": th,
        "04_opened": opened,
        "05_edges_canny": edges,
        "06_overlay_edges": overlay,
    }


def save_outputs(outputs: dict[str, np.ndarray], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for name, img in outputs.items():
        # Tentukan ext berdasarkan tipe (gray/edge tetap jpg aman; edge juga bisa png)
        ext = ".jpg"
        if name.endswith("edges_canny"):
            ext = ".png"
        path = outdir / f"{name}{ext}"
        ok = cv2.imwrite(str(path), img)
        if not ok:
            print(f"WARNING: gagal menyimpan {path}")


def show_outputs_matplotlib(outputs: dict[str, np.ndarray]) -> None:
    """Tampilkan hasil gambar dengan matplotlib."""
    def show(title: str, img: np.ndarray, is_gray: bool = False) -> None:
        plt.figure()
        plt.title(title)
        plt.axis("off")
        if is_gray:
            plt.imshow(img, cmap="gray")
        else:
            plt.imshow(bgr_to_rgb(img))

    show("Input (resized)", outputs["00_input_resized"], is_gray=False)
    show("Grayscale", outputs["01_gray"], is_gray=True)
    show("Blurred (Gaussian)", outputs["02_blurred"], is_gray=True)
    show("Threshold (Otsu)", outputs["03_threshold_otsu"], is_gray=True)
    show("Morphology: Open", outputs["04_opened"], is_gray=True)
    show("Edges (Canny)", outputs["05_edges_canny"], is_gray=True)
    show("Overlay edges (green)", outputs["06_overlay_edges"], is_gray=False)
    plt.show()


def run_image_test(image_path: str | None, show: bool, no_save: bool, outdir: Path) -> int:
    print("=== OpenCV Installation Test (Image) ===")
    print("OpenCV version:", cv2.__version__)

    # Load image jika ada, kalau tidak -> synthetic
    img_bgr: np.ndarray
    if image_path:
        p = Path(image_path)
        if p.exists():
            img_bgr = safe_imread(p)
            if img_bgr is None:
                print("WARNING: cv2.imread gagal, memakai gambar sintetis.")
                img_bgr = generate_synthetic_image()
            else:
                print(f"Loaded image: {p} | shape={img_bgr.shape}")
        else:
            print(f"WARNING: file tidak ditemukan: {p} -> memakai gambar sintetis.")
            img_bgr = generate_synthetic_image()
    else:
        print("Tidak ada path gambar -> memakai gambar sintetis.")
        img_bgr = generate_synthetic_image()

    outputs = process_image(img_bgr)

    if not no_save:
        save_outputs(outputs, outdir)
        print("Output saved to:", outdir.resolve())
    else:
        print("Mode --no-save aktif: tidak menyimpan output.")

    if show:
        show_outputs_matplotlib(outputs)
    else:
        print("Mode tanpa tampilan. Gunakan --show untuk menampilkan hasil.")

    return 0


def run_webcam_test(cam_index: int, show: bool, duration: int, no_save: bool, outdir: Path) -> int:
    """
    Uji webcam realtime.
    - Tekan 'q' untuk keluar lebih cepat
    - Ambil snapshot terakhir jika tidak --no-save
    Catatan: untuk webcam, 'show' dianjurkan (cv2.imshow). Jika show=False, kita tetap proses
    tapi tidak membuka jendela; hanya uji capture + simpan snapshot.
    """
    print("=== OpenCV Installation Test (Webcam) ===")
    print("OpenCV version:", cv2.__version__)
    print(f"Trying to open camera index: {cam_index}")

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("ERROR: Webcam tidak bisa dibuka.")
        print("Coba:")
        print("  - ganti index: --cam-index 1 (atau 2)")
        print("  - cek permission kamera (Windows/macOS)")
        return 2

    print("Webcam terbuka.")
    if show:
        print("Tekan 'q' untuk keluar. Akan berjalan selama ~", duration, "detik.")
    else:
        print("show=False: tidak membuka jendela. Akan jalan selama ~", duration, "detik.")

    last_frame = None
    t0 = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            print("ERROR: gagal membaca frame dari webcam.")
            break

        last_frame = frame
        outputs = process_image(frame)

        if show:
            cv2.imshow("Webcam - Input", outputs["00_input_resized"])
            cv2.imshow("Webcam - Gray", outputs["01_gray"])
            cv2.imshow("Webcam - Edges", outputs["05_edges_canny"])
            cv2.imshow("Webcam - Overlay edges", outputs["06_overlay_edges"])

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Keluar (q).")
                break

        if (time.time() - t0) >= duration:
            print("Selesai (duration).")
            break

    cap.release()
    if show:
        cv2.destroyAllWindows()

    if last_frame is None:
        print("ERROR: tidak ada frame yang berhasil diambil.")
        return 2

    if not no_save:
        outdir.mkdir(parents=True, exist_ok=True)
        # Simpan snapshot proses terakhir
        snap_outputs = process_image(last_frame)
        save_outputs(snap_outputs, outdir)
        print("Snapshot output saved to:", outdir.resolve())
    else:
        print("Mode --no-save aktif: tidak menyimpan snapshot.")

    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenCV install test: image pipeline + optional webcam test."
    )
    parser.add_argument(
        "image",
        nargs="?",
        default=None,
        help="Path gambar (opsional). Jika kosong, gunakan gambar sintetis.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Tampilkan hasil. (Gambar: matplotlib, Webcam: cv2.imshow)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Tidak menyimpan output ke folder.",
    )
    parser.add_argument(
        "--outdir",
        default="output_test",
        help="Folder untuk menyimpan output (default: output_test).",
    )
    parser.add_argument(
        "--webcam",
        action="store_true",
        help="Jalankan pengujian webcam realtime.",
    )
    parser.add_argument(
        "--cam-index",
        type=int,
        default=0,
        help="Index kamera (default: 0). Coba 1 jika 0 gagal.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Durasi uji webcam (detik), default: 10.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    outdir = Path(args.outdir)

    # Mode webcam atau gambar
    if args.webcam:
        # Untuk webcam, "show" sangat membantu; tapi tetap boleh false (headless)
        return run_webcam_test(
            cam_index=args.cam_index,
            show=args.show,
            duration=args.duration,
            no_save=args.no_save,
            outdir=outdir,
        )
    else:
        return run_image_test(
            image_path=args.image,
            show=args.show,
            no_save=args.no_save,
            outdir=outdir,
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
