import cv2
import numpy as np
import os
from t_14 import CircularLinkedListOneway

# base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/'
# image = cv2.imread(base_path + 't.jpg')
# image = cv2.resize(image, (200, 200*np.shape(image)[0]//np.shape(image)[1]))
# h, w, c = np.shape(image)
# v_list = CircularLinkedListOneway()
# [v_list.append(i) for i in ['俊      .', '❤      .', '婷      .']]
# # [v_list.append(i) for i in ['狗      .', '葱       .', '则       .']]
# node = v_list.link_head()
# html_file = open(base_path + '4.html', 'w')
# html_head = '<!DOCTYPE html>\n' + \
#             '<html lang="en">\n' + \
#             '<style>\n' + \
#             '    html {\n' + \
#             '        -webkit-filter: grayscale(100%);\n' + \
#             '        -moz-filter: grayscale(100%);\n' + \
#             '        -ms-filter: grayscale(100%);\n' + \
#             '        -o-filter: grayscale(100%);\n' + \
#             '        filter:progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);\n' + \
#             '        _filter:none;\n' + \
#             '    }\n' + \
#             '</style>\n' + \
#             '<head>\n' + \
#             '    <meta charset="UTF-8">\n' + \
#             '    <title>Title</title>\n' + \
#             '</head>\n' + \
#             '<body>\n'
# html_tail = '</body>\n' + \
#             '</html>\n'
# html_file.write(html_head)
# # html_file.write('<div style="width:3px;"><br/>')
# for i in range(h):
#     for j in range(w):
#         node = v_list.next_node(node)
#         color = '#' + hex(image[i, j][2]).replace('0x', '') + hex(image[i, j][1]).replace('0x', '') + hex(image[i, j][0]).replace('0x', '')
#         content = node.value
#         html_cell = '<font style="line-height:0.05;" color="' + color + '" size="1">' + content + '</font>'
#         html_file.write(html_cell)
#     html_file.write('<br/>')
# html_file.write(html_tail)

from PIL import Image, ImageDraw, ImageFont


# def cv2ImgAddText(img, text, left, top, textColor=150, textSize=20):
#     img = Image.fromarray(img)
#     draw = ImageDraw.Draw(img)
#     fontStyle = ImageFont.truetype("/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/simsun/simsun.ttc", textSize, encoding="utf-8")
#     draw.text((left, top), text, textColor, font=fontStyle)
#     return np.asarray(img)
#
# base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/'
# ori_image = cv2.imread(base_path + 'c_1.jpg', 0)
# ori_image = cv2.resize(ori_image, (200, 200*np.shape(ori_image)[0]//np.shape(ori_image)[1]))
# h, w = np.shape(ori_image)
# pix = 30
# out_image = np.ones((pix*np.shape(ori_image)[0], pix*np.shape(ori_image)[1]), dtype=np.uint8) * 255
#
# v_list = CircularLinkedListOneway()
# [v_list.append(i) for i in ['狗      .', '葱       .', '则       .']]
# node = v_list.link_head()
# for i in range(h):
#     print(i)
#     for j in range(w):
#         node = v_list.next_node(node)
#         content = node.value
#         patch_image = np.ones((pix, pix), dtype=np.uint8) * 255
#         patch_image = cv2ImgAddText(patch_image, node.value, 0, 0, textColor=int(ori_image[i, j]//2), textSize=pix)
#         out_image[i*pix:(i+1)*pix, j*pix:(j+1)*pix] = patch_image
#         # cv2.imshow('out_image', patch_image)
#         # cv2.waitKey()
#
# cv2.imwrite(base_path + 'c_out.jpg', out_image)
# cv2.imshow('out_image', cv2.resize(out_image, (w, h)))
# cv2.waitKey()

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/simsun/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/'
ori_image = cv2.imread(base_path + 't.jpg')
ori_image = cv2.resize(ori_image, (100, 100 * np.shape(ori_image)[0] // np.shape(ori_image)[1]))
h, w, _ = np.shape(ori_image)
pix = 30
out_image = np.ones((pix * np.shape(ori_image)[0], pix * np.shape(ori_image)[1], 3), dtype=np.uint8) * 255

v_list = CircularLinkedListOneway()
# [v_list.append(i) for i in ['狗', '葱', '则']]
[v_list.append(i) for i in ['美', '婷', '婷']]
node = v_list.link_head()
for i in range(h):
    print(i)
    for j in range(w):
        node = v_list.next_node(node)
        content = node.value
        patch_image = np.ones((pix, pix, 3), dtype=np.uint8) * 255
        patch_image = cv2ImgAddText(patch_image, node.value, 0, 0, textColor=(int(ori_image[i, j][2]), int(ori_image[i, j][1]), int(ori_image[i, j][0])), textSize=pix)
        out_image[i * pix:(i + 1) * pix, j * pix:(j + 1) * pix] = patch_image
        # cv2.imshow('out_image', patch_image)
        # cv2.waitKey()

cv2.imwrite(base_path + 't_out.jpg', out_image)
cv2.imshow('out_image', cv2.resize(out_image, (w, h)))
cv2.waitKey()
