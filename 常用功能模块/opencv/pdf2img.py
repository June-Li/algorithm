import io
import os
import fitz
import cv2
import numpy as np
import PIL as PI
from PIL import Image


def pdf2img(pdf_path, log_file):
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
        try:
            image_pdf = Image(filename=pdf_path, resolution=200)
            with image_pdf.convert('jpg') as conv:
                for img in conv.sequence:
                    img_page = Image(image=img).make_blob('jpg')
                    image = io.BytesIO(img_page)
                    img = np.array(PI.open(image).convert('RGB'))
                    image_list.append(img)
        except:
            log_file.write(pdf_path + '\n')
    return image_list

base_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/'
in_path = base_path + 'pdf/'
out_path = base_path + 'images/'
log_file = open(base_path + 'tran_error.txt', 'w')
pdf_name_list = os.listdir(in_path)
total_img_num = 0
for count, pdf_name in enumerate(pdf_name_list):
    images = pdf2img(in_path + pdf_name, log_file)
    total_img_num += len(images)
    for index, image in enumerate(images):
        # if pdf_name.startswith('20滇池投资CP'):
        #     image = np.rot90(image, -1)
        cv2.imwrite(out_path + pdf_name[::-1].split('.', 1)[-1][::-1] + '_' + str(index) + '.jpg', image)
    if count % 100 == 0:
        print('processed num: ', count+1, '    current total imgs: ', total_img_num)
print('total imgs: ', total_img_num)
