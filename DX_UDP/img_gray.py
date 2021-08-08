
#encoding:UTF-8
__author__ = 'DX'

# import cv2 as cv
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

    byte16_s = '0b'
    byte17_s = '0b'
    byte18_s = '0b'
    byte19_s = '0b'
    byte20_s = '0b'
    byte21_s = '0b'
    byte22_s = '0b'
    byte23_s = '0b'
    byte24_s = '0b'
    byte25_s = '0b'
    byte26_s = '0b'
    byte27_s = '0b'
    byte28_s = '0b'
    byte29_s = '0b'
    byte30_s = '0b'

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

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte8_s = byte8_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte9_s = byte9_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte10_s = byte10_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte11_s = byte11_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte12_s = byte12_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte13_s = byte13_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte14_s = byte14_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte15_s = byte15_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte16_s = byte16_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte17_s = byte17_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte18_s = byte18_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte19_s = byte19_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte20_s = byte20_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte21_s = byte21_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte22_s = byte22_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte23_s = byte23_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte24_s = byte24_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte25_s = byte25_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte26_s = byte26_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte27_s = byte27_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte28_s = byte28_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte29_s = byte29_s + b_s[i]

    # bit_start = bit_start + 8
    # bit_end = bit_end + 8
    # if((bit_start < img_w) and (bit_end < img_w)):
    #     for i in range(bit_start,bit_end,-1): 
    #         byte30_s = byte30_s + b_s[i]


    # 返回图片宽度为112像素
    # return (eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s), \
    #         eval(byte6_s), eval(byte7_s), eval(byte8_s), eval(byte9_s), eval(byte10_s), \
    #         eval(byte11_s), eval(byte12_s), eval(byte13_s), eval(byte14_s))
            
    # 返回图片宽度为240像素
    # return (eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s), \
    #         eval(byte6_s), eval(byte7_s), eval(byte8_s), eval(byte9_s), eval(byte10_s), \
    #         eval(byte11_s), eval(byte12_s), eval(byte13_s), eval(byte14_s), eval(byte15_s), \
    #         eval(byte16_s), eval(byte17_s), eval(byte18_s), eval(byte19_s), eval(byte20_s), \
    #         eval(byte21_s), eval(byte22_s), eval(byte23_s), eval(byte24_s), eval(byte25_s), \
    #         eval(byte26_s), eval(byte27_s), eval(byte28_s), eval(byte29_s), eval(byte30_s))

    # # 返回图片宽度为56像素
    return (eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s), \
            eval(byte6_s), eval(byte7_s))

    # 返回图片宽度为120像素
    # return (eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s), \
    #         eval(byte6_s), eval(byte7_s), eval(byte8_s), eval(byte9_s), eval(byte10_s), \
    #         eval(byte11_s), eval(byte12_s), eval(byte13_s), eval(byte14_s), eval(byte15_s))

    # return eval(byte1_s), eval(byte2_s), eval(byte3_s), eval(byte4_s), eval(byte5_s)
    # return hex(eval(byte1_s)), hex(eval(byte2_s)), hex(eval(byte3_s)), hex(eval(byte4_s)), hex(eval(byte5_s))
    # return eval(byte1_s), eval(byte2_s)


def img_to_bin():
    index_i = 0
    # img = Image.open('Location Pin.jpg')
    # img = Image.open('wifi.jpg')   #16*16
    # img = Image.open('test111.jpg')  #120*232
    img = Image.open('/home/dx/sites/dx1023.com/django_blog/media/images/chinese.jpg')  #56*59
    # img = Image.open('chinese.jpg')  #56*59
    # img = Image.open('/home/dx/sites/dx1023.com/django_blog/media/images/json_pic.jpg')  #240*135  112*59
    # img = Image.open('json_pic.jpg')  #240*135  112*59
    
    img_w = img.width   # 图片的宽
    img_h = img.height  # 图片的高
    gray = img.convert('1')  #将图片转换成黑白位图 L
    data = asarray(gray)
    # print('图片共有')
    # print(data.size)
    # print('-----------点------------')              #每8个点组成1个字节
    
    # 图片的宽决定了data[i]中包含为的大小，X的像素值就是data[i]中包含元素的大小
    # 图片的长决定了data[i]中i的大小

    # print(data[0])  #0-15  True-0  False-1
    # print(data[1])
    # print(data[2])
    # print(data[3])

    image_sizeByets = int(data.size/8)
    # print(image_sizeByets)

    image_sizeGroup = img_h   #int(image_sizeByets/2)
   
    #创建固定尺寸图字节数组
    image_b = [0 for i in range(image_sizeByets)]
    # image_b = [0 for i in range(img_w * img_h)]

    # img.convert('L')  #将图片转换成黑白位图--获得图像
    # for i in range(0,img_h):
    #     for data_index in range(img.width):
    #         image_b[index_i] = data[i][data_index]
    #         index_i = index_i + 1


    # 获得整张图片二进制值  图片像素 112
    # for i in range(0,image_sizeGroup):
    #     image_b[i*14], image_b[(i*14)+1], image_b[(i*14)+2], image_b[(i*14)+3], image_b[(i*14)+4], \
    #     image_b[(i*14)+5], image_b[(i*14)+6], image_b[(i*14)+7], image_b[(i*14)+8], image_b[(i*14)+9], \
    #     image_b[(i*14)+10], image_b[(i*14)+11], image_b[(i*14)+12], image_b[(i*14)+13] = get_img_2Bytes(data[i], img_w)

    # 获得整张图片二进制值  图片像素 240
    # for i in range(0,image_sizeGroup):
    #     image_b[i*30], image_b[(i*30)+1], image_b[(i*30)+2], image_b[(i*30)+3], image_b[(i*30)+4], \
    #     image_b[(i*30)+5], image_b[(i*30)+6], image_b[(i*30)+7], image_b[(i*30)+8], image_b[(i*30)+9], \
    #     image_b[(i*30)+10], image_b[(i*30)+11], image_b[(i*30)+12], image_b[(i*30)+13], image_b[(i*30)+14], \
    #     image_b[(i*30)+15], image_b[(i*30)+16], image_b[(i*30)+17], image_b[(i*30)+18], image_b[(i*30)+19], \
    #     image_b[(i*30)+20], image_b[(i*30)+21], image_b[(i*30)+22], image_b[(i*30)+23], image_b[(i*30)+24], \
    #     image_b[(i*30)+25], image_b[(i*30)+26], image_b[(i*30)+27], image_b[(i*30)+28], image_b[(i*30)+29]  = get_img_2Bytes(data[i], img_w)

    # 获得整张图片二进制值  图片像素 56--img.convert('1')
    for i in range(0,image_sizeGroup):
        image_b[i*7], image_b[(i*7)+1], image_b[(i*7)+2], image_b[(i*7)+3], image_b[(i*7)+4], \
        image_b[(i*7)+5], image_b[(i*7)+6] = get_img_2Bytes(data[i], img_w)

    # 获得整张图片二进制值  图片像素 120
    # for i in range(0,image_sizeGroup):
    #     image_b[i*15], image_b[(i*15)+1], image_b[(i*15)+2], image_b[(i*15)+3], image_b[(i*15)+4], \
    #     image_b[(i*15)+5], image_b[(i*15)+6], image_b[(i*15)+7], image_b[(i*15)+8], image_b[(i*15)+9], \
    #     image_b[(i*15)+10], image_b[(i*15)+11], image_b[(i*15)+12], image_b[(i*15)+13], image_b[(i*15)+14] = get_img_2Bytes(data[i], img_w)

    # 图片像素 16
    # image_b[0], image_b[1] = get_img_2Bytes(data[0])

    # 将数据写入文件
    # file = open('data.txt','w')
    # file.write(str(image_b))
    # file.close()

    # # 获得完整图片位图数组
    # image_b[0] = eval(byte1_s)
    # image_b[1] = eval(byte2_s)

    # print(image_b)
    # print(hex(image_b[0]))
    # print(hex(image_b[1]))

    # gray.show()

    return (image_b)

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

# img_to_bin()

