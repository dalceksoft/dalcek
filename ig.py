import os
import instaloader
from urllib.parse import urlparse

L = instaloader.Instaloader(
    download_videos=True,
    download_video_thumbnails=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern="",
    dirname_pattern="downloads/{target}",
    filename_pattern="{date_utc}_UTC",
)

def extract_shortcode(url: str):
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) >= 2 and parts[0] in ("p", "reel", "tv"):
        return parts[1]

    return None


def download_post(url: str):
    shortcode = extract_shortcode(url)

    if not shortcode:
        print("❌ Link hatalı.")
        return

    try:
        os.makedirs("downloads", exist_ok=True)

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        print("⬇️ İndiriliyor...")
        L.download_post(post, target="post_reel")

        print("✅ Tamamlandı.")

    except Exception as e:
        print("❌ Hata:", e)


def main():
    print("Instagram Reel / Post Downloader")

    while True:

        url = input("\nInstagram linki gir (çıkmak için q): ").strip()

        if url.lower() == "q":
            break

        download_post(url)


if __name__ == "__main__":
    main()
