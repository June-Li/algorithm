import glob
import unittest
import pandas as pd
import pdfplumber
from pdfplumber import utils
from pdfplumber import table
import sys, os
# from wand.image import Image
import numpy as np
import cv2
from shutil import copyfile

# pdf_list = []
# Annotation_dir = '/home/sxs/yuhsuan/data/generate_scan/Annotations/'
# Annotation_list=glob.glob(Annotation_dir+'*.xml')
# filedir = '/home/sxs/yuhsuan/data/personal_check/pdf'
# savedir = '/home/sxs/yuhsuan/data/generate_scan/extra/'
# for file in Annotation_list:
# 	file = file.split('/')[-1]
# 	file = file[:-4].split('_')[0]
# 	pdf_list.append(file+'.PDF')

# pdf_list = set(pdf_list)
# for file in pdf_list:
# 	path = os.path.join(filedir,file)
# 	print('processing......',path)
# 	if not os.path.isfile(path):
# 		continue
# 	pdf = pdfplumber.open(path)

# 	num_pages=len(pdf.pages)
# 	directory=os.path.join(savedir)
# 	# directory_JPEG=os.path.join(savedir,'JPEG',file[:-4])
# 	# text_directory=os.path.join(savedir,'location',file[:-4])
# 	if not os.path.exists(directory):
# 		os.mkdir(directory)
# 	# if not os.path.exists(text_directory):
# 	# 	os.mkdir(text_directory)
# 	for index in range(num_pages):

# 		self=pdf.pages[index]
# 		tables=self.find_tables()
# 		print(index)
# 		if tables:
# 			for j in range(len(tables)):
# 				table_arr=tables[j].extract()
# 				# for m in range(len(table_arr)):
# 					# for n in range(len(table_arr[m])):
# 					# 	cell=tables[j].rows[m]
# 				if len(table_arr) ==1:
# 					savename=file[:-4]+'_page_'+str(index)+'.xml'
# 					copyfile(os.path.join(Annotation_dir,savename),os.path.join(directory,savename))
# 						# if cell is None:
# 						# 	continue
# 						# cell_text=table_arr[m][n]
# directory = '/home/sxs/yuhsuan/data/generate_scan/extra/'
new_dir = '/home/sxs/yuhsuan/data/generate_scan/Annotations'
img_dir = '/home/sxs/yuhsuan/data/generate_scan/scan_no_rotate_after'
file_list = glob.glob(new_dir + '/*.xml')
# for file in file_list:
# 	new = file.split('/')[-1]
# 	new_file = new[:-4]+'_1.xml'
# 	copyfile(file,os.path.join(new_dir,new_file))
# 	copyfile(os.path.join(img_dir,new[:-4]+'.jpg'),os.path.join(img_dir,new[:-4]+'_1.jpg'))			
for file in file_list:
    new = file.split('/')[-1]
    if not os.path.isfile(os.path.join(img_dir, new[:-4] + '.jpg')):
        # copyfile(os.path.join('/home/sxs/yuhsuan/data/generate_scan/JPEG_after',new[:-4]+'.jpg'),os.path.join(img_dir,new[:-4]+'.jpg'))
        print(new)
