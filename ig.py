import os
import time
from datetime import datetime
from urllib.parse import urlparse

import instaloader

DOWNLOAD_DIR = "/storage/emulated/0/Movies"

L = instaloader.Instaloader(
    download_videos=True,
    download_video_thumbnails=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern="",
    dirname_pattern=DOWNLOAD_DIR,
    filename_pattern="{shortcode}",
    quiet=False,
    max_connection_attempts=1,
)


def extract_shortcode(url: str):
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) >= 2 and parts[0] in ("p", "reel", "tv"):
        return parts[1]

    return None


def media_scan(path: str):
    os.system(f'termux-media-scan "{path}" > /dev/null 2>&1')


def set_now_mtime(path: str):
    now = time.time()
    os.utime(path, (now, now))


def list_media_files(folder: str):
    if not os.path.exists(folder):
        return set()

    out = set()
    for name in os.listdir(folder):
        full = os.path.join(folder, name)
        if os.path.isfile(full) and name.lower().endswith((".mp4", ".jpg", ".jpeg", ".png", ".webp")):
            out.add(full)
    return out


def download_post(url: str):
    shortcode = extract_shortcode(url)

    if not shortcode:
        print("❌ Link hatalı.")
        return

    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        before = list_media_files(DOWNLOAD_DIR)

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        print("⬇️ En iyi mevcut kalite indiriliyor...")
        L.download_post(post, target=".")

        after = list_media_files(DOWNLOAD_DIR)
        new_files = sorted(after - before)

        # Yeni dosya bulunamazsa kısa kodla başlayanları bul
        if not new_files:
            candidates = []
            for f in after:
                base = os.path.basename(f)
                if base.startswith(shortcode):
                    candidates.append(f)
            new_files = sorted(candidates)

        if not new_files:
            print("⚠️ Dosya indirildi gibi görünüyor ama yeni dosya yolu tespit edilemedi.")
            print(f"📁 Klasör: {DOWNLOAD_DIR}")
            return

        # Yeni dosyaların zamanını şimdi yap
        for f in new_files:
            set_now_mtime(f)

        media_scan(DOWNLOAD_DIR)

        print("✅ Tamamlandı.")
        print("📁 Kaydedilen dosyalar:")
        for f in new_files:
            size_mb = os.path.getsize(f) / (1024 * 1024)
            print(f"- {f} ({size_mb:.2f} MB)")

        print("🎬 Galeride Movies kısmını kontrol et.")

    except Exception as e:
        print("❌ Hata:", e)


def main():
    print("Instagram Reel / Post Downloader")

    while True:
        url = input("\nInstagram linki gir (çıkmak için q): ").strip()

        if url.lower() == "q":
            print("Çıkılıyor...")
            break

        download_post(url)


if __name__ == "__main__":
    main()
