from bs4 import BeautifulSoup
import os
import time
import requests
from urllib.parse import urljoin, urlparse

def get_image_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            # urljoinを使用して絶対URLを生成
            absolute_url = urljoin(base_url, src)
            urls.append(absolute_url)
    
    return urls

def download_images(image_urls, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for src in image_urls:
        try:
            img_data = requests.get(src).content
            # urlparseを使用してファイル名を取得し、クエリパラメータを無視
            file_name = os.path.join(folder_name, os.path.basename(urlparse(src).path))
            with open(file_name, 'wb') as file:
                file.write(img_data)
            print(f"Downloaded: {file_name}")
            time.sleep(1)  # サーバーへの負担を減らすための遅延
        except Exception as e:
            print(f"Failed to download {src}: {e}")

def main():
    url = 'https://XXXX.YYY'  # 画像をダウンロードしたいウェブページのURL
    folder_name = 'downloaded_images'  # 画像を保存するフォルダの名前
    
    # 画像のURLを取得
    image_urls = get_image_urls(url)
    print(f"Found {len(image_urls)} images.")
    
    # 画像をダウンロード
    download_images(image_urls, folder_name)

if __name__ == "__main__":
    main()
