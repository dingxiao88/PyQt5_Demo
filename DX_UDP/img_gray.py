
#encoding:UTF-8
__author__ = 'DX'

import cv2 as cv
import requests
from PIL import Image
from numpy import asarray


def get_img_2Bytes(input_data, img_w):

     # 创建img_w bit位元素
    b = [0 for i in range(img_w)]
    # 创建img_w bit字符位元素
    b_s = ['0' for i in range(img_w)]

    # 获得img_w 位img_w/8字节位图元素
    for i in range(img_w):
        b[i] = input_data[i]
        if(b[i] == True):
            b_s[i] = '0'
        elif(b[i] == False):
            b_s[i] = '1'
        i = i - 1

    # 获得2字节位图元素
    byte1_s = '0b'
    byte2_s = '0b'
    byte3_s = '0b'
    byte4_s = '0b'
    byte5_s = '0b'
    byte6_s = '0b'
    byte7_s = '0b'
    byte8_s = '0b'
    byte9_s = '0b'
    byte10_s = '0b'
    byte11_s = '0b'
    byte12_s = '0b'
    byte13_s = '0b'
    byte14_s = '0b'
    byte15_s = '0b'

    #从7到0进行遍历循环，括号里最后一个-1是步长，实现倒序；前两个参数是起始和终止值，也是前闭后开。
    for i in range(7,-1,-1): 
        byte1_s = byte1_s + b_s[i]

    bit_start = 7 + 8
    bit_end = -1 + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        #从15到7进行遍历循环
        for i in range(bit_start,bit_end,-1): 
            byte2_s = byte2_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte3_s = byte3_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte4_s = byte4_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte5_s = byte5_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte6_s = byte6_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte7_s = byte7_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte8_s = byte8_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte9_s = byte9_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte10_s = byte10_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte11_s = byte11_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte12_s = byte12_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte13_s = byte13_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte14_s = byte14_s + b_s[i]

    bit_start = bit_start + 8
    bit_end = bit_end + 8
    if((bit_start < img_w) and (bit_end < img_w)):
        for i in range(bit_start,bit_end,-1): 
            byte15_s = byte15_s + b_s[i]

    return (eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s), \
            eval(byte6_s), eval(byte7_s), eval(byte8_s), eval(byte9_s), eval(byte10_s), \
            eval(byte11_s), eval(byte12_s), eval(byte13_s), eval(byte14_s), eval(byte15_s))


    # return eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s)
    # return hex(eval(byte1_s)), hex(eval(byte2_s)), hex(eval(byte3_s)), hex(eval(byte4_s)), hex(eval(byte5_s))
    # return eval(byte1_s), eval(byte2_s)


def img_to_bin():
    # img = Image.open('Location Pin.jpg')
    # img = Image.open('wifi.jpg')
    img = Image.open('test111.jpg')
    img_w = img.width   # 图片的宽
    img_h = img.height  # 图片的高
    gray = img.convert('1')  #将图片转换成黑白位图
    data = asarray(gray)
    print('图片共有')
    print(data.size)
    print('-----------点------------')              #每8个点组成1个字节
    
    # 图片的宽决定了data[i]中包含为的大小，X的像素值就是data[i]中包含元素的大小
    # 图片的长决定了data[i]中i的大小

    # print(data[0])  #0-15  True-0  False-1
    # print(data[1])
    # print(data[2])
    # print(data[3])

    image_sizeByets = int(data.size/8)

    image_sizeGroup = img_h   #int(image_sizeByets/2)
   
    #创建固定尺寸图字节数组
    image_b = [0 for i in range(image_sizeByets)]

    # 获得整张图片二进制值
    for i in range(0,image_sizeGroup):
        image_b[i*15], image_b[(i*15)+1], image_b[(i*15)+2], image_b[(i*15)+3], image_b[(i*15)+4], \
        image_b[(i*15)+5], image_b[(i*15)+6], image_b[(i*15)+7], image_b[(i*15)+8], image_b[(i*15)+9], \
        image_b[(i*15)+10], image_b[(i*15)+11], image_b[(i*15)+12], image_b[(i*15)+13], image_b[(i*15)+14] = get_img_2Bytes(data[i], img_w)
        # image_b[i*2], image_b[(i*2)+1] = get_img_2Bytes(data[i], img_w)

    # image_b[0], image_b[1] = get_img_2Bytes(data[0])

    file = open('data.txt','w')
    file.write(str(image_b))
    file.close()


    # # 获得完整图片位图数组
    # image_b[0] = eval(byte1_s)
    # image_b[1] = eval(byte2_s)

    print(image_b)
    # print(hex(image_b[0]))
    # print(hex(image_b[1]))

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

# img_png_to_jpg()

img_to_bin()

