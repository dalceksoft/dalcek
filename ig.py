import os
from urllib.parse import urlparse

import instaloader
from instaloader.exceptions import (
    BadResponseException,
    ConnectionException,
    LoginRequiredException,
    PostChangedException,
    QueryReturnedBadRequestException,
    TooManyRequestsException,
)

DOWNLOAD_BASE = "/storage/emulated/0/Download"

L = instaloader.Instaloader(
    download_videos=True,
    download_video_thumbnails=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern="",
    dirname_pattern=os.path.join(DOWNLOAD_BASE, "{target}"),
    filename_pattern="{date_utc}_UTC",
    quiet=False,
    max_connection_attempts=1,
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
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        print("⬇️ İndiriliyor...")
        L.download_post(post, target="post_reel")
        print("✅ Tamamlandı.")
        print(f"📁 Kayıt yeri: {DOWNLOAD_BASE}/post_reel/")

    except TooManyRequestsException:
        print("❌ 429 Too Many Requests. Biraz bekleyip tekrar dene.")
    except LoginRequiredException:
        print("❌ Bu içerik için giriş gerekli olabilir.")
    except (BadResponseException, QueryReturnedBadRequestException, PostChangedException) as e:
        print(f"❌ Gönderi bilgisi alınamadı: {e}")
    except ConnectionException as e:
        print(f"❌ Bağlantı hatası: {e}")
    except Exception as e:
        print(f"❌ Hata: {e}")


def main():
    print("Instagram Reel / Post Downloader (Termux)")

    while True:
        url = input("\nInstagram linki gir (çıkmak için q): ").strip()

        if url.lower() == "q":
            print("Çıkılıyor...")
            break

        download_post(url)


if __name__ == "__main__":
    main()
