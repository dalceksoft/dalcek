import os
import re
import json
import requests
from html import unescape
from urllib.parse import urlparse

DOWNLOAD_DIR = "downloads"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 14; Termux) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Mobile Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def ensure_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip() or "instagram_media"


def extract_shortcode(url: str) -> str | None:
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 2 and parts[0] in ("p", "reel", "tv"):
        return parts[1]
    return None


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 2 and parts[0] in ("p", "reel", "tv"):
        return f"https://www.instagram.com/{parts[0]}/{parts[1]}/"
    return url.strip()


def fetch_html(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def find_meta_content(html: str, key: str) -> str | None:
    patterns = [
        rf'<meta[^>]+property="{re.escape(key)}"[^>]+content="([^"]+)"',
        rf'<meta[^>]+content="([^"]+)"[^>]+property="{re.escape(key)}"',
        rf"<meta[^>]+property='{re.escape(key)}'[^>]+content='([^']+)'",
        rf"<meta[^>]+content='([^']+)'[^>]+property='{re.escape(key)}'",
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            return unescape(m.group(1))
    return None


def find_json_media(html: str) -> tuple[str | None, str | None]:
    # Ek fallback: bazen meta tag yerine JSON içinde oluyor
    video_match = re.search(r'"video_url":"(https:[^"]+)"', html)
    image_match = re.search(r'"display_url":"(https:[^"]+)"', html)

    video_url = None
    image_url = None

    if video_match:
        video_url = video_match.group(1).replace("\\u0026", "&").replace("\\/", "/")
    if image_match:
        image_url = image_match.group(1).replace("\\u0026", "&").replace("\\/", "/")

    return video_url, image_url


def resolve_media(url: str) -> tuple[str | None, str | None]:
    html = fetch_html(url)

    # Önce og meta
    video_url = find_meta_content(html, "og:video")
    image_url = find_meta_content(html, "og:image")

    # Sonra JSON fallback
    if not video_url and not image_url:
        j_video, j_image = find_json_media(html)
        video_url = video_url or j_video
        image_url = image_url or j_image

    return video_url, image_url


def download_file(url: str, out_path: str):
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)


def download_instagram_media(url: str):
    clean_url = normalize_url(url)
    shortcode = extract_shortcode(clean_url)

    if not shortcode:
        print("❌ Geçersiz Instagram reel/gönderi linki.")
        return

    try:
        print("🔎 Medya aranıyor...")
        video_url, image_url = resolve_media(clean_url)

        if video_url:
            filename = sanitize_filename(f"{shortcode}.mp4")
            out_path = os.path.join(DOWNLOAD_DIR, filename)
            print("⬇️ Video indiriliyor...")
            download_file(video_url, out_path)
            print(f"✅ İndirildi: {out_path}")
            return

        if image_url:
            ext = ".jpg"
            if ".png" in image_url.lower():
                ext = ".png"
            elif ".webp" in image_url.lower():
                ext = ".webp"

            filename = sanitize_filename(f"{shortcode}{ext}")
            out_path = os.path.join(DOWNLOAD_DIR, filename)
            print("⬇️ Görsel indiriliyor...")
            download_file(image_url, out_path)
            print(f"✅ İndirildi: {out_path}")
            return

        print("❌ Medya URL'si bulunamadı.")
        print("Bu linkte Instagram sayfa yapısı değişmiş olabilir ya da içerik erişime kapalı olabilir.")

    except requests.HTTPError as e:
        print(f"❌ HTTP hatası: {e}")
    except Exception as e:
        print(f"❌ Hata: {e}")


def main():
    ensure_download_dir()
    print("Instagram Reel / Gönderi Downloader (Termux)")

    while True:
        url = input("\nInstagram linki gir (çıkmak için q): ").strip()
        if url.lower() == "q":
            break
        download_instagram_media(url)


if __name__ == "__main__":
    main()
