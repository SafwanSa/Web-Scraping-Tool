from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageChops
import numpy as np

def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def is_new(img):
    if len(imgs) == 0:
        imgs.append(img)
    else:
        dup = False
        for prev_img in imgs:
            bol = equal(prev_img, img)
            if bol:
                dup = True
        if not dup:
            imgs.append(img)
            return not dup
        else:
            return dup

counter = 0
imgs = []

for i in range(30):
    source = requests.get('https://www.stockvault.net/c/animals/cats-and-dogs/?s=l&p={}'.format(i)).text
    
    soup = BeautifulSoup(source, 'lxml')
    
    page_wrap = soup.find_all('div', class_='clearfix', id='wrapper')
    
    content = page_wrap[0].find('div', id='content')
    
    rows = content.find_all('div', class_='section nomargin nopadding')
    
    for row in rows:
        items = row.find_all('div', class_='item')
        for item in items:
            # print(item.a.img)
            image = item.a.img
            image_url = image['src']

            try:
                img = Image.open(requests.get(image_url, stream=True).raw)
            except:
                pass
            img_name = 'image_{}.jpg'.format(counter)
            if is_new(img):
                img.save('Images/{}'.format(img_name))
                counter += 1
                print(counter)
