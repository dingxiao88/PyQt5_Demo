

# # https://gist.github.com/hidsh/7065820

# #! /usr/bin/env python
# # -*- coding: utf-8 -*-

# from PIL import Image
# import struct, os, sys

# def usage():
#     print ('./png2rgb565.py HOGE.png')
#     sys.exit(1)
    
# def error(msg):
#     print (msg)
#     sys.exit(-1)
    
# def write_bin(f, pixel_list):
#     for pix in pixel_list:
#         r = (pix[0] >> 3) & 0x1F
#         g = (pix[1] >> 2) & 0x3F
#         b = (pix[2] >> 3) & 0x1F
#         f.write(struct.pack('H', (r << 11) + (g << 5) + b))

# ##
# if __name__ == '__main__':
#     args = sys.argv
#     if len(args) != 2: usage()
#     in_path = args[1]
#     if os.path.exists(in_path) == False: error('not exists: ' + in_path)
    
#     body, _ = os.path.splitext(in_path)
#     out_path = body + '.bin'

#     img = Image.open(in_path).convert('RGB')
#     pixels = list(img.getdata())
#     # print pixels
    
#     with open(out_path, 'wb') as f:
#         write_bin(f, pixels)

# # -----------------------------------------------------------------------


# https://blog.csdn.net/weixin_37598106/article/details/116700903
#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@ Summary: img2rgb565() 函数将图片保存为 RGB565
           show_rgb565() 将rgb565反转为rgb888并显示图片
@ Update:  

@ file:    png2rgb565.py
@ version: 1.0.0

@ Author:  Lebhoryi@gmail.com
@ Date:    2021/5/11 18:41
@ Link:    https://github.com/jimmywong2003/PNG-to-RGB565/blob/master/png2rgb565.py

@ Example:
            python png2rgb565.py NRF52840_DK_ILI9341.png NRF52840_DK.h NRF52840.bin
'''
import sys
from PIL import Image
import struct
import cv2
import numpy as np

isSWAP = False

def img2rgb565():
    len_argument = len(sys.argv)
    if (len_argument != 4):
        print("")
        print("Correct Usage:")
        print("\tpython png2rgb565.py <png_file> <include_file> <binary_file>")
        print("")
        sys.exit(0)

    try:
        im = Image.open(sys.argv[1])
    except:
        raise Exception(f"Fail to open png file {sys.argv[1]}")

    image_height = im.size[1]
    image_width = im.size[0]

    try:
        outfile = open(sys.argv[2], "w")
    except:
        raise Exception(f"Can't write the file {sys.argv[2]}")


    try:
        binoutfile = open(sys.argv[3], "wb")
    except:
        raise Exception(f"Can't write the binary file {im.size[3]}")


    print(f"/* Image Width:{im.size[0]} Height:{im.size[1]} */", file=outfile)
    print("const static uint16_t Hand_10[] = {", file=outfile)

    pix = im.load()  # load pixel array
    for h in range(image_height):
        for w in range(image_width):
            if ((h * 16 + w) % 16 == 0):
                print(" ", file=outfile)
                print("\t\t", file=outfile, end='')

            if w < im.size[0]:
                R = pix[w, h][0] >> 3
                G = pix[w, h][1] >> 2
                B = pix[w, h][2] >> 3

                rgb = (R << 11) | (G << 5) | B

                if (isSWAP == True):
                    swap_string_low = rgb >> 8
                    swap_string_high = (rgb & 0x00FF) << 8
                    swap_string = swap_string_low | swap_string_high
                    print("0x%04x, " % (swap_string), file=outfile, end='')
                    binoutfile.write(struct.pack('H', swap_string))
                else:
                    print("%04d, " % (rgb), file=outfile, end='')
                    binoutfile.write(struct.pack('H', rgb))
            else:
                rgb = 0

    print("", file=outfile)
    print("};", file=outfile)

    outfile.close()
    binoutfile.close()

    print(f"Image file {sys.argv[1]} converted to {sys.argv[2]} done.")
    return sys.argv[2]


def show_rgb565(img_file):
    # Read 16-bit RGB565 image into array of uint16
    with open(img_file, 'r') as f:
        lines = f.read().split()
    lines = lines[11:-1]
    lines = list(map(lambda i: int(i[:-1]), lines))
    image = np.array(lines)
    # rgb565array = np.reshape(image, (224, 224))
    rgb565array = np.reshape(image, (270, 270))


    # Pick up image dimensions
    h, w = rgb565array.shape

    # Make a numpy array of matching shape, but allowing for 8-bit/channel for R, G and B
    rgb888array = np.zeros([h, w, 3], dtype=np.uint8)

    for row in range(h):
        for col in range(w):
            # Pick up rgb565 value and split into rgb888
            rgb565 = rgb565array[row, col]
            r = ((rgb565 >> 11) & 0x1f) << 3
            g = ((rgb565 >> 5) & 0x3f) << 2
            b = ((rgb565) & 0x1f) << 3
            # Populate result array
            rgb888array[row, col] = r, g, b

    # Save result as PNG
    # Image.fromarray(rgb888array).save('result.png')
    rgb888array = cv2.cvtColor(rgb888array, cv2.COLOR_RGB2BGR)
    cv2.imshow("result", rgb888array)
    cv2.waitKey(2000)
    cv2.destroyWindow("result")


def main():
    img_file = img2rgb565()
    show_rgb565(img_file)

if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------------------

# # https://github.com/jimmywong2003/PNG-to-RGB565/blob/master/png2rgb565.py

# #!/usr/bin/python

# import sys
# import os

# from PIL import Image
# from PIL import ImageDraw
# import struct

# isSWAP = False
# # isSWAP = True

# def main():

#     len_argument = len(sys.argv)
#     filesize = 0
#     if (len_argument != 4):
#       print ("")
#       print ("Correct Usage:")
#       print ("\tpython png2rgb565.py <png_file> <include_file> <binary_file>")
#       print ("")
#       sys.exit(0)

#     try:
#         im=Image.open(sys.argv[1])
#         #print ("/* Image Width:%d Height:%d */" % (im.size[0], im.size[1]))
#     except:
#         print ("Fail to open png file ", sys.argv[1])
#         sys.exit(0)

#     image_height = im.size[1]
#     image_width = im.size[0]

#     try:
#         outfile = open(sys.argv[2],"w")
#     except:
#         print ("Can't write the file %s" % sys.argv[2])
#         sys.exit(0)

#     try:
#         binoutfile = open(sys.argv[3],"wb")
#     except:
#         print ("Can't write the binary file %s" % sys.argv[3])
#         sys.exit(0)


#     print ("/* Image Width:%d Height:%d */" % (im.size[0], im.size[1]), file=outfile)
#     print ("const static uint16_t image_640_240_jimmy[] = {", file=outfile)

#     pix = im.load()  #load pixel array
#     for h in range(image_height):
#         for w in range(image_width):
#             if ((h * 16 + w) % 16 == 0):
#                 print (" ", file=outfile)
#                 print ("\t\t", file=outfile, end = '')

#             if w < im.size[0]:
#                 R=pix[w,h][0]>>3
#                 G=pix[w,h][1]>>2
#                 B=pix[w,h][2]>>3

#                 rgb = (R<<11) | (G<<5) | B

#                 if (isSWAP == True):
#                     swap_string_low = rgb >> 8
#                     swap_string_high = (rgb & 0x00FF) << 8
#                     swap_string = swap_string_low | swap_string_high
#                     print ("0x%04x," %(swap_string), file=outfile, end = '')
#                     binoutfile.write(struct.pack('H', swap_string))
#                 else:
#                     print ("0x%04x," %(rgb), file=outfile, end = '')
#                     binoutfile.write(struct.pack('H', rgb))
#             else:
#                 rgb = 0
#         #
#     print ("", file=outfile)
#     print ("};", file=outfile)

#     outfile.close()
#     binoutfile.close()

#     print ("PNG file \"%s\"" % sys.argv[1], "converted to \"%s\"" % sys.argv[2])

# if __name__=="__main__":
#   main()




#  python -m lvgl.converter --output_format bin_565 --color_format true_color me.png