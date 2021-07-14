
#encoding:UTF-8
__author__ = 'DX'

import cv2 as cv
import requests
from PIL import Image
from numpy import asarray


def img_to_bin():
    img = Image.open('Location Pin.jpg')
    gray = img.convert('1')
    data = asarray(gray)
    print(data.size)
    print(data[0][0])  //0-15
    # print(data[1])
    # print(data[2])
    # print(data[3])

    gray.show()

    # opencv方法
    # img = cv.imread('index.jpg',1)
    # img_1 = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # cv.imwrite('index_gray.jpg', img_1)
    # cv.imshow('gray',img_1)
    # cv.imshow('colour',img)
    # cv.waitKey(0)

def img_png_to_jpg():
    image_url = "https://www.zazhipdf.com/wp-content/themes/rizhuti/timthumb.php?src=https://www.zazhipdf.com/wp-content/uploads/2021/07/da9ded8acca6cc1.png&h=270&w=270&zc=1&a=c&q=100&s=1"
    
    img_data = requests.get(image_url).content
    with open('image_name.png', 'wb') as handler:
        handler.write(img_data)

    im = Image.open('image_name.png')
    rgb_im = im.convert('RGB')
    rgb_im.save('img_png_to_jpg.jpg')

img_png_to_jpg()
