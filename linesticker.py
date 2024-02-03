import json
import msvcrt
import os

import apnggif
import bs4
import requests
from moviepy.editor import *

while True:
    number = input('輸入貼圖編號：')
    print()

    # 設定爬取貼圖網址
    url = 'https://store.line.me/stickershop/product/' + number
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')

    # 圖片目錄
    image_dir = 'image/'
    now_dir = image_dir + number
    png_dir = now_dir + '/png/'
    gif_dir = now_dir + '/gif/'
    sound_dir = now_dir + '/sound/'
    output_dir = now_dir + '/output/'

    # 建資料夾
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    if not os.path.exists(now_dir):
        os.mkdir(now_dir)
    if not os.path.exists(png_dir):
        os.mkdir(png_dir)

    # 下載貼圖
    Data = soup.select('li[class*="mdCMN09Li FnStickerPreviewItem"]')
    count = 0
    for data in Data:
        # 將字串資料轉換為字典
        img_info = json.loads(data.get('data-preview'))
        ID = img_info['id']

        # 如果有動圖就存動圖檔(apng[檔名一樣是.png])
        if img_info['animationUrl']:
            img_file = requests.get(img_info['animationUrl'])
            animate = True
            sound=False
            if not os.path.exists(gif_dir):
                os.mkdir(gif_dir)
        #如果是有音檔的動圖
        elif img_info['popupUrl']:
            img_file = requests.get(img_info['popupUrl'])
            animate = True
            sound=True
            if not os.path.exists(gif_dir):
                os.mkdir(gif_dir)
            sound_file=requests.get(img_info['soundUrl'])
            if not os.path.exists(sound_dir):
                os.mkdir(sound_dir)
        else:
            img_file = requests.get(img_info['staticUrl'])
            animate = False
            sound=False

        # 儲存的路徑和主檔名
        png_path = os.path.join(png_dir, ID)

        # 儲存圖片
        with open(png_path + '.png', 'wb') as f:
            f.write(img_file.content)

        # 將apng轉換成gif
        if animate:
            gif_path = os.path.join(gif_dir, ID)
            apnggif.apnggif(png_path + '.png', gif_path + '.gif')
        if sound:
            sound_path = os.path.join(sound_dir, ID)
            with open(sound_path + '.m4a', 'wb') as f:
                f.write(sound_file.content)
            gif_clip = VideoFileClip(gif_path + '.gif')
            audio_clip = AudioFileClip(sound_path + '.m4a')
            gif_clip = gif_clip.set_audio(audio_clip)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            output_file = os.path.join(output_dir, ID + ".mp4")
            gif_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")


        if not count and animate:
            print('此貼圖為動圖，將順便另存為gif檔')
            print()

        count += 1

    print('成功下載' + count.__str__() + '張貼圖')
    print('按Enter鍵下載其他貼圖，其他鍵離開程式')

    # 決定是否繼續下載
    if ord(msvcrt.getch()) != 13:
        break
    else:
        print()
