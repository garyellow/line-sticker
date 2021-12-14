import json
import os
import bs4
import requests
import apnggif

number = input('輸入貼圖編號：')

# 設定爬取貼圖網址
url = 'https://store.line.me/stickershop/product/' + number
html = requests.get(url)
soup = bs4.BeautifulSoup(html.text, 'html.parser')

# 圖片目錄
image_dir = 'image/'
png_dir = 'image/png/'
gif_dir = 'image/gif/'

# 建資料夾
if not os.path.exists(image_dir):
    os.mkdir(image_dir)
if not os.path.exists(png_dir):
    os.mkdir(png_dir)

# 下載貼圖
Data = soup.find_all('li', {'class': 'mdCMN09Li FnStickerPreviewItem'})
for data in Data:
    # 將字串資料轉換為字典
    img_info = json.loads(data.get('data-preview'))
    ID = img_info['id']

    # 如果有動圖就從動圖檔(apng[檔名一樣是.png])
    if img_info['animationUrl']:
        img_file = requests.get(img_info['animationUrl'])
        animate = True
        if not os.path.exists(gif_dir):
            os.mkdir(gif_dir)
    else:
        img_file = requests.get(img_info['staticUrl'])
        animate = False

    # 儲存的路徑和主檔名
    png_path = os.path.join(png_dir, ID)

    # 儲存圖片           
    with open(png_path + '.png', 'wb') as f:
        f.write(img_file.content)

    # 將apng轉換成gif
    if animate:
        gif_path = os.path.join(gif_dir, ID)
        apnggif.apnggif(png_path + '.png', gif_path + '.gif')
