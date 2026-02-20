import cv2


def main() -> int:
    cap = cv2.VideoCapture(0)  # coba 0, kalau gagal coba 1
    if not cap.isOpened():
        print("ERROR: Webcam tidak bisa dibuka. Coba ganti index (0/1) atau cek permission.")
        return 2

    print("Tekan 'q' untuk keluar.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("ERROR: gagal membaca frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        cv2.imshow("Webcam - Original", frame)
        cv2.imshow("Webcam - Gray", gray)
        cv2.imshow("Webcam - Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
