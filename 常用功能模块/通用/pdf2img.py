import os
import io
import cv2
import numpy as np
import fitz
import PIL as PI
from PIL import Image, ImageDraw, ImageFont


def pdf2img(pdf_path, max_len):
    try:
        doc = fitz.open(pdf_path)
        for page_index, page in enumerate(doc):
            trans = fitz.Matrix(2.0, 2.0).preRotate(0)
            pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
            getpngdata = pm.getImageData(output="png")
            # 解码为 np.uint8
            image_array = np.frombuffer(getpngdata, dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_ANYCOLOR)
            h, w, _ = np.shape(img)
            if max(h, w) > max_len:
                if h > w:
                    img = cv2.resize(img, (max_len * w // h, max_len))
                else:
                    img = cv2.resize(img, (max_len, max_len * h // w))
            yield img
    except:
        image_pdf = Image(filename=pdf_path, resolution=200)
        with image_pdf.convert('jpg') as conv:
            for img in conv.sequence:
                img_page = Image(image=img).make_blob('jpg')
                image = io.BytesIO(img_page)
                img = np.array(PI.open(image).convert('RGB'))
                h, w, _ = np.shape(img)
                if max(h, w) > max_len:
                    if h > w:
                        img = cv2.resize(img, (max_len * w // h, max_len))
                    else:
                        img = cv2.resize(img, (max_len, max_len * h // w))
                yield img