## preprocess
# step1: pdf2png
# step2: do pdfplumber to get ground truth
# step3: 
import os
import cv2
import argparse
import glob
import numpy as np
from wand.image import Image
import xml.dom.minidom
import pdfplumber
from pdfplumber import utils
from pdfplumber import table
import unittest
# import generate_bbox
# import makexml
import pandas as pd


def load_data(input_data_dir, output_data_dir):
    pdf_list = []
    pdf_file_dir = []
    print(input_data_dir)
    pdf_file = glob.glob(input_data_dir + '/*.pdf')
    pdf_file.extend(glob.glob(input_data_dir + '/*.PDF'))
    print('Processing......', pdf_file)
    for category in pdf_file:
        if category.startswith('.'):
            continue
        pdf_dir = os.path.join(output_data_dir, category.split('/')[-1][:-4])
        if os.path.exists(pdf_dir):
            pass
        else:
            os.mkdir(pdf_dir)
        pdf_list.append(category)
        pdf_file_dir.append(pdf_dir)
    return pdf_list, pdf_file_dir


def Pdf2Image(pdfpath, filepath, resolution_para=1200):
    '''
    function: convert pdf to processed images

    input: pdf path(from argparse), threshold value th(default=190), image resolution(default=460)
    output: a list of image file names
    '''
    image_pdf = Image(filename=pdfpath, resolution=resolution_para)

    with image_pdf.convert('jpg') as conv:
        conv.save(filename=os.path.join(filepath, 'page.jpg'))


def image2small(data_dir, save_dir, save_tran_dir):
    n = 0
    for pdf in data_dir:
        pages = os.listdir(pdf)
        for page in pages:
            image = cv2.imread(os.path.join(pdf, page))
            h, w, z = image.shape
            # print(h,w)
            # 6600,5100
            image = cv2.resize(image, (496, 702))
            # print(image.shape)
            name = str(n)
            s = name.zfill(6)
            cv2.imwrite(os.path.join(save_dir, s + '.jpg'), image)
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # perform transformations on image
            b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
            g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
            r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)

            # merge the transformed channels back to an image
            transformed_image = cv2.merge((b, g, r))
            target_file = os.path.join(save_tran_dir, s + '.jpg')
            cv2.imwrite(target_file, transformed_image)
            n += 1


def makefile(dirname, name, bbox, size, num_of_pos=1):
    doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)

    nodeManager = doc.createElement('folder')
    nodeManager.appendChild(doc.createTextNode('personal'))
    root.appendChild(nodeManager)
    nodeManager = doc.createElement('filename')
    nodeManager.appendChild(doc.createTextNode(name + '.jpg'))
    root.appendChild(nodeManager)
    nodeManager = doc.createElement('source')

    nodedata = doc.createElement('database')
    nodedata.appendChild(doc.createTextNode('The personal table Database'))
    nodeanno = doc.createElement('annotation')
    nodeanno.appendChild(doc.createTextNode('PASCAL VOC2007'))
    nodeimage = doc.createElement('image')
    nodeimage.appendChild(doc.createTextNode('flickr'))
    nodeflick = doc.createElement('flickrid')
    nodeflick.appendChild(doc.createTextNode('334966661'))

    nodeManager.appendChild(nodedata)
    nodeManager.appendChild(nodeanno)
    nodeManager.appendChild(nodeimage)
    nodeManager.appendChild(nodeflick)
    root.appendChild(nodeManager)
    ###size
    nodeManager = doc.createElement('size')

    nodewidth = doc.createElement('width')
    nodewidth.appendChild(doc.createTextNode(str(size[1])))
    nodeheight = doc.createElement('height')
    nodeheight.appendChild(doc.createTextNode(str(size[0])))
    nodedepth = doc.createElement('depth')
    nodedepth.appendChild(doc.createTextNode(str(size[2])))

    nodeManager.appendChild(nodewidth)
    nodeManager.appendChild(nodeheight)
    nodeManager.appendChild(nodedepth)
    root.appendChild(nodeManager)
    ### segmented
    print(len(bbox))
    ## object
    # if len(bbox)>0 or num_of_pos%10==0:
    #   text_file = open(os.path.join(dirname,'Textfile',name+'.txt'), "w")
    #   text_file.write(str(len(bbox)))
    #   text_file.write('\n')
    for box in bbox:
        nodeManager = doc.createElement('object')

        nodename = doc.createElement('name')
        nodename.appendChild(doc.createTextNode('Table'))
        nodepose = doc.createElement('pose')
        nodepose.appendChild(doc.createTextNode('Unspecified'))
        nodetrun = doc.createElement('truncated')
        nodetrun.appendChild(doc.createTextNode('0'))
        nodediff = doc.createElement('difficult')
        nodediff.appendChild(doc.createTextNode('1'))
        ## bndbox
        nodebbox = doc.createElement('bndbox')
        nodexmin = doc.createElement('xmin')
        nodexmin.appendChild(doc.createTextNode(str(box[0])))
        nodeymin = doc.createElement('xmax')
        nodeymin.appendChild(doc.createTextNode(str(box[1])))
        nodexmax = doc.createElement('ymin')
        nodexmax.appendChild(doc.createTextNode(str(box[2])))
        nodeymax = doc.createElement('ymax')
        nodeymax.appendChild(doc.createTextNode(str(box[3])))
        nodebbox.appendChild(nodexmin)
        nodebbox.appendChild(nodeymin)
        nodebbox.appendChild(nodexmax)
        nodebbox.appendChild(nodeymax)
        ###
        nodeManager.appendChild(nodename)
        nodeManager.appendChild(nodepose)
        nodeManager.appendChild(nodetrun)
        nodeManager.appendChild(nodediff)
        nodeManager.appendChild(nodebbox)
        root.appendChild(nodeManager)
        # text_file.write(','.join(box))

    # if bbox or num_of_pos%10==0:
    fp = open(os.path.join(dirname, 'Annotations', name + '.xml'), 'w')  # change
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="ISO-8859-1")
    # box=[str(x1),str(x2),str(y1),str(y2)]                 
    # return 1
    return 1


def get_bbox(pdfpath, filepath, rootdir, n):
    print('processing......', pdfpath, filepath)
    pdf = pdfplumber.open(pdfpath)
    num_pages = len(pdf.pages)
    for index in range(num_pages):
        path = os.path.join(filepath, 'page-' + str(index) + '.jpg')
        name = str(n).zfill(6)
        if num_pages == 1:
            path = os.path.join(filepath, 'page.jpg')
        self = pdf.pages[index]
        image = cv2.imread(path)
        ###############
        # 6600,5100
        image = cv2.resize(image, (5100, 6600))
        cv2.imwrite(os.path.join(rootdir, 'JPEG', name + '.jpg'), image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # perform transformations on image
        b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
        g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
        r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)
        # merge the transformed channels back to an image
        transformed_image = cv2.merge((b, g, r))
        target_file = os.path.join(rootdir, 'JPEG_after', name + '.jpg')
        cv2.imwrite(target_file, transformed_image)
        #################
        scale_x, scale_y = 5100 / self.width, 6600 / self.height
        tables = self.find_tables()

        text_file = open(os.path.join(rootdir, 'Textfile', name + '.txt'), "w")
        box_list = []
        text_file.write(str(len(tables)))
        text_file.write('\n')
        if tables:

            for table in tables:
                bbox = table.bbox
                x1, y1, x2, y2 = int(bbox[0] * scale_x), int(bbox[1] * scale_y), int(bbox[2] * scale_x), int(
                    bbox[3] * scale_y)
                # A=img[y1:y2,x1:x2]
                cv2.rectangle(image, (x1, y1), (x2, y2), (179, 255, 255), 100)
                box = [str(x1), str(x2), str(y1), str(y2)]
                text_file.write(','.join(box))
                text_file.write('\n')
                box_list.append(box)

        T = makefile(rootdir, name, box_list, image.shape, num_of_pos=1)

        cv2.imwrite(os.path.join(rootdir, 'SegmentationObject', name + '.jpg'), image)
        text_file.close()
        n += 1
    return n


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--root',
        dest='rootdir',
        type=str,
        default='/home/sxs/yuhsuan/data/test_data',
        help="input data directory"
    )
    parser.add_argument(
        '--input',
        dest='input',
        type=str,
        default='/home/sxs/yuhsuan/data/test_data/PDF',
        help="input data directory"
    )
    parser.add_argument(
        '--output',
        dest='output',
        type=str,
        default='/home/sxs/yuhsuan/data/test_data/png',
        help="output directory"
    )
    parser.add_argument(
        '--size',
        dest='size',
        type=int,
        default=0,
        help="Number of pdf in each file. size=0 refers to all file"
    )
    options = parser.parse_args()
    input_data_dir = options.input
    output_data_dir = options.output
    rootdir = options.rootdir
    num_per_class = options.size
    if os.path.exists(os.path.join(rootdir, 'png')):
        pass
    else:
        os.mkdir(os.path.join(rootdir, 'JPEG'))
        os.mkdir(os.path.join(rootdir, 'JPEG_after'))
        # os.mkdir(os.path.join(rootdir,'PDF'))
        os.mkdir(os.path.join(rootdir, 'SegmentationObject'))
        os.mkdir(os.path.join(rootdir, 'Textfile'))
        os.mkdir(os.path.join(rootdir, 'png'))
        os.mkdir(os.path.join(rootdir, 'Image_after'))

    data_list, data_dir = load_data(input_data_dir, output_data_dir)
    # step 1
    # for i, fname in enumerate(data_list):
    #     outputDir = Pdf2Image(data_list[i], data_dir[i])

    # step2-1 We need to move image to different place. cut and resize image
    print('step2.........')
    image2small(data_dir, os.path.join(rootdir, 'JPEG'), os.path.join(rootdir, 'JPEG_after'))

    ## step2-2 Get the ground truth bbox
    # n=0
    # for i, fname in enumerate(data_list):
    #     n = get_bbox(data_list[i], data_dir[i],rootdir,n)
