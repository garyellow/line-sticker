import requests
import os
import json
from bs4 import BeautifulSoup

number = input('輸入貼圖編號：')

url = 'https://store.line.me/stickershop/product/' + number
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

# 圖片目錄
images_dir = "image/"
if not os.path.exists(images_dir):
    os.mkdir(images_dir)

# 下載貼圖
Data = soup.find_all('li', {'class': 'mdCMN09Li FnStickerPreviewItem'})
for data in Data:
    # 將字串資料轉換為字典
    img_info = json.loads(data.get('data-preview'))
    ID = img_info['id']
    img_file = requests.get(img_info['staticUrl'])

    # 儲存的路徑和主檔名
    full_path = os.path.join(images_dir, ID)

    # 儲存圖片           
    with open(full_path + '.png', 'wb') as f:
        f.write(img_file.content)
