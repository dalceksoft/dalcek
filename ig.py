import os
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
    filename_pattern="{date_utc}_UTC",
)

def extract_shortcode(url):
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) >= 2 and parts[0] in ("p", "reel", "tv"):
        return parts[1]

    return None


def download_post(url):

    shortcode = extract_shortcode(url)

    if not shortcode:
        print("❌ Link hatalı.")
        return

    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        print("⬇️ İndiriliyor...")

        L.download_post(post, target=".")

        print("✅ Tamamlandı.")
        print("📁 Video galeride Movies klasöründe")

    except Exception as e:
        print("❌ Hata:", e)


while True:

    url = input("\nInstagram linki gir (çıkmak için q): ").strip()

    if url.lower() == "q":
        break

    download_post(url)
