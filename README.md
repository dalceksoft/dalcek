# Instagram Reel / Post Downloader

Instagram **reel** ve **post** linklerinden medya indirmek için basit bir Python scripti.

---

## Özellikler

- Reel indirir  
- Post indirir  
- Otomatik dosya adı verir  
- Telefon ve PC uyumlu  

---

## Gereksinimler

- Python 3  
- pip  

---

# Telefon Kurulumu (Termux)

## 1) Paketleri kur

```bash
pkg update && pkg upgrade -y
pkg install python -y
pkg install termux-api -y
```

## 2) Kütüphane yükle

```bash
pip install instaloader
```

## 3) Depolama izni ver

```bash
termux-setup-storage
```

## 4) Çalıştır

```bash
cd dalcek
python ig.py
```

---

# PC Kurulumu

## 1) Python kontrol et

```bash
python --version
```

## 2) Projeyi indir

```bash
git clone https://github.com/dalceksoft/dalcek.git
cd dalcek
```

## 3) Kütüphane kur

```bash
pip install -r requirements.txt
```

Alternatif:

```bash
pip install instaloader
```

## 4) Çalıştır

```bash
python ig.py
```

---

# Kullanım

Program açıldığında link girmeniz istenir:

```text
Instagram linki gir (çıkmak için q):
```

Örnek linkler:

```text
https://www.instagram.com/reel/XXXX/
https://www.instagram.com/p/XXXX/
```

Linki yapıştır → Enter → İndirme başlar.

---

# Çıkış

```text
q
```

---

# Kayıt Yeri

Varsayılan kayıt klasörü:

```python
DOWNLOAD_DIR = "/storage/emulated/0/Movies"
```

- Telefonda → Galeri > Movies  
- PC'de → Aşağıdan değiştirebilirsiniz  

---

# PC için Klasör Değiştirme

Kod içindeki şu satırı değiştirin:

```python
DOWNLOAD_DIR = "/storage/emulated/0/Movies"
```

Örnekler:

Windows:
```python
DOWNLOAD_DIR = "C:/Users/Kullanici/Downloads"
```

Linux:
```python
DOWNLOAD_DIR = "/home/kullanici/Downloads"
```

Mac:
```python
DOWNLOAD_DIR = "/Users/kullanici/Downloads"
```

---

# Desteklenen Linkler

- /p/  
- /reel/  
- /tv/  

---

# Olası Hatalar

## instaloader hatası

```bash
pip install instaloader
```

## termux-media-scan hatası

```bash
pkg install termux-api -y
```

## İndirme olmuyorsa

- Link yanlış olabilir  
- Post gizli olabilir  
- İçerik silinmiş olabilir  

---

# Dosyalar

- ig.py  
- requirements.txt  

---

# Hızlı Başlatma

## Telefon

```bash
pkg update && pkg upgrade -y
pkg install python -y
pkg install termux-api -y
termux-setup-storage
pip install instaloader
python ig.py
```

## PC

```bash
git clone https://github.com/dalceksoft/dalcek.git
cd dalcek
pip install instaloader
python ig.py
```

---

# Uyarı

Bu araç kişisel kullanım içindir.  
İndirilen içeriklerin haklarına dikkat edin.

---

# Lisans

Kişisel kullanım.
