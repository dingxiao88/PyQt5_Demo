
#encoding:UTF-8
__author__ = 'DX'

import cv2 as cv
from PIL import Image

from numpy import asarray

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
