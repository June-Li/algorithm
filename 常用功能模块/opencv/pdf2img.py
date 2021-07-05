import io
import os
import fitz
import cv2
import numpy as np
import PIL as PI
from PIL import Image


def pdf2img(pdf_path):
    image_list = []
    try:
        doc = fitz.open(pdf_path)
        for page_index, page in enumerate(doc):
            trans = fitz.Matrix(2.0, 2.0).preRotate(0)
            pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
            getpngdata = pm.getImageData(output="png")
            # 解码为 np.uint8
            image_array = np.frombuffer(getpngdata, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
            image_list.append(img)
    except:
        image_pdf = Image(filename=pdf_path, resolution=200)
        with image_pdf.convert('jpg') as conv:
            for img in conv.sequence:
                img_page = Image(image=img).make_blob('jpg')
                image = io.BytesIO(img_page)
                img = np.array(PI.open(image).convert('RGB'))
                image_list.append(img)
    return image_list

base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/'
in_path = base_path + '华泰样本/'
out_path = base_path + '华泰样本-图片/'
pdf_name_list = os.listdir(in_path)
for pdf_name in pdf_name_list:
    images = pdf2img(in_path + pdf_name)
    for index, image in enumerate(images):
        if pdf_name.startswith('20滇池投资CP'):
            image = np.rot90(image, -1)
        cv2.imwrite(out_path + pdf_name.replace('.pdf', '_') + str(index) + '.jpg', image)
    print()
