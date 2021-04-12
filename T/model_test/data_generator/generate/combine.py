## combine.py
# This is for combing bg, file and seal
import cv2
import numpy as np
import os
import math
import random
import glob


def crop(Img):
    H, W, z = Img.shape
    y = H / 2 + 20
    x = W / 2 + 60
    winW = random.randrange(100, x - 60)
    winH = random.randrange(80, y - 20)
    # cv2.rectangle(rotateImg, (int(x-winW), int(y-winH)), (int(x + winW), int(y + winH)), (0, 255, 0), 2)
    # cv2.imshow('tfimg',rotateImg)
    # cv2.waitKey(0)
    # cropImg_clone = rotateImg.copy()
    cropImg = Img[int(y - winH):int(y + winH), int(x - winW):int(x + winW), :]
    return cropImg


def rotate_bound(image, angle=1.5):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))


# def makefile(bbox,img,name,num_of_pos=1):
#     size=img.shape
#     doc=xml.dom.minidom.Document()
#     root=doc.createElement('annotation')
#     doc.appendChild(root)

#     nodeManager=doc.createElement('folder')
#     nodeManager.appendChild(doc.createTextNode('scannedfile')) 
#     root.appendChild(nodeManager)
#     nodeManager=doc.createElement('filename')
#     nodeManager.appendChild(doc.createTextNode(name))  
#     root.appendChild(nodeManager)
#     nodeManager=doc.createElement('source')

#     nodedata=doc.createElement('database')
#     nodedata.appendChild(doc.createTextNode('The personal table Database'))
#     nodeanno=doc.createElement('annotation')
#     nodeanno.appendChild(doc.createTextNode('PASCAL VOC2007'))
#     nodeimage=doc.createElement('image')
#     nodeimage.appendChild(doc.createTextNode('flickr'))
#     nodeflick=doc.createElement('flickrid')
#     nodeflick.appendChild(doc.createTextNode('334966661'))

#     nodeManager.appendChild(nodedata)
#     nodeManager.appendChild(nodeanno)
#     nodeManager.appendChild(nodeimage)
#     nodeManager.appendChild(nodeflick)
#     root.appendChild(nodeManager)
#     ###size
#     nodeManager=doc.createElement('size')

#     nodewidth=doc.createElement('width')
#     nodewidth.appendChild(doc.createTextNode(str(size[0])))
#     nodeheight=doc.createElement('height')
#     nodeheight.appendChild(doc.createTextNode(str(size[1])))
#     nodedepth=doc.createElement('depth')
#     nodedepth.appendChild(doc.createTextNode(str(3)))

#     nodeManager.appendChild(nodewidth)
#     nodeManager.appendChild(nodeheight)
#     nodeManager.appendChild(nodedepth)
#     root.appendChild(nodeManager)
#     ### segmented

#     print(len(bbox))
#     ## object
#     # if len(bbox)>0 or num_of_pos%10==0:
#     #   text_file = open(os.path.join(dirname,'Textfile',name+'.txt'), "w")
#     #   text_file.write(str(len(bbox)))
#     #   text_file.write('\n')
#     for box in bbox:
#         nodeManager=doc.createElement('object')
#         nodename=doc.createElement('name')
#         nodename.appendChild(doc.createTextNode('Text'))
#         nodepose=doc.createElement('pose')
#         nodepose.appendChild(doc.createTextNode('Unspecified'))
#         nodetrun=doc.createElement('truncated')
#         nodetrun.appendChild(doc.createTextNode('0'))
#         nodediff=doc.createElement('difficult')
#         nodediff.appendChild(doc.createTextNode('1'))
#         ## bndbox
#         nodebbox=doc.createElement('bndbox')
#         nodexmin=doc.createElement('xmin')
#         nodexmin.appendChild(doc.createTextNode(str(box[0])))
#         nodeymin=doc.createElement('ymin')
#         nodeymin.appendChild(doc.createTextNode(str(box[1])))
#         nodexmax=doc.createElement('xmax')
#         nodexmax.appendChild(doc.createTextNode(str(box[2])))
#         nodeymax=doc.createElement('ymax')
#         nodeymax.appendChild(doc.createTextNode(str(box[3])))
#         nodebbox.appendChild(nodexmin)
#         nodebbox.appendChild(nodeymin)
#         nodebbox.appendChild(nodexmax)
#         nodebbox.appendChild(nodeymax)
#         ###
#         nodeManager.appendChild(nodename)
#         nodeManager.appendChild(nodepose)
#         nodeManager.appendChild(nodetrun)
#         nodeManager.appendChild(nodediff)
#         nodeManager.appendChild(nodebbox)
#         root.appendChild(nodeManager)
#         # text_file.write(','.join(box))
#     for box in freeze:
#         nodeManager=doc.createElement('object')
#         nodename=doc.createElement('name')
#         nodename.appendChild(doc.createTextNode('Table'))
#         nodepose=doc.createElement('pose')
#         nodepose.appendChild(doc.createTextNode('Unspecified'))
#         nodetrun=doc.createElement('truncated')
#         nodetrun.appendChild(doc.createTextNode('0'))
#         nodediff=doc.createElement('difficult')
#         nodediff.appendChild(doc.createTextNode('1'))
#         ## bndbox
#         nodebbox=doc.createElement('bndbox')
#         nodexmin=doc.createElement('xmin')
#         nodexmin.appendChild(doc.createTextNode(str(box[0])))
#         nodeymin=doc.createElement('ymin')
#         nodeymin.appendChild(doc.createTextNode(str(box[1])))
#         nodexmax=doc.createElement('xmax')
#         nodexmax.appendChild(doc.createTextNode(str(box[2])))
#         nodeymax=doc.createElement('ymax')
#         nodeymax.appendChild(doc.createTextNode(str(box[3])))
#         nodebbox.appendChild(nodexmin)
#         nodebbox.appendChild(nodeymin)
#         nodebbox.appendChild(nodexmax)
#         nodebbox.appendChild(nodeymax)
#         ###
#         nodeManager.appendChild(nodename)
#         nodeManager.appendChild(nodepose)
#         nodeManager.appendChild(nodetrun)
#         nodeManager.appendChild(nodediff)
#         nodeManager.appendChild(nodebbox)
#         root.appendChild(nodeManager)            
#     # if bbox or num_of_pos%10==0:

#     fp = open(os.path.join(self.rootDir,'Annotations',name[:-4]+'.xml'), 'w') # change
#     doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="ISO-8859-1")
#     # box=[str(x1),str(x2),str(y1),str(y2)]                 
#         # return 1
#     return 1

# rootdir='/Users/sd/Desktop/generate_scan/'
rootdir = '/Volumes/my_disk/company/sensedeal/PycharmProject/test/data_generator/datasets/'
bg_list = glob.glob(os.path.join('/Volumes/my_disk/company/sensedeal/PycharmProject/test/data_generator/generate', 'bg', '*.png'))
ink_list = glob.glob(os.path.join('/Volumes/my_disk/company/sensedeal/PycharmProject/test/data_generator/generate', 'ink', '*jpg'))
# seal_list=glob.glob(os.path.join(rootdir,'seal'))
num_bg = len(bg_list)
num_ink = len(ink_list)
# num_seal=len(seal_list)
bg = [cv2.imread(os.path.join(path)) for path in bg_list]
ink = [cv2.imread(os.path.join(path)) for path in ink_list]
# seal=[cv2.imread(os.path.join(path)) for path in seal_list]
# load image
image_list = glob.glob(os.path.join(rootdir, 'super_resolution3', '*.jpg'))
for path in image_list:
    name = path.split('/')[-1]
    # print(os.path.join(rootdir,'JPEG',name.replace('txt', 'jpg')))
    orig_no = cv2.imread(os.path.join(rootdir, 'super_resolution3', name.replace('jpg', 'jpg')))
    mask_no = cv2.imread(os.path.join(rootdir, 'super_resolution_mask3', name.replace('jpg', 'jpg')))
    print(mask_no.shape)
    h_o, w_o, z = orig_no.shape
    alpha = random.randint(-5, 5)
    # print(alpha)
    theta = math.radians(alpha)
    # orig = rotate_bound(orig_no,alpha)
    # mask = rotate_bound(mask_no,alpha)
    orig = orig_no
    mask = mask_no
    h, w, z = orig.shape
    # print(random.randint(0,num_bg-1))
    select_bg = bg[random.randint(0, num_bg - 1)]
    select_ink = ink[random.randint(0, num_ink - 1)]
    # random crop
    select_bg = crop(select_bg)
    # resize
    select_bg = cv2.resize(select_bg, (w, h))
    select_ink = cv2.resize(select_ink, (w, h))
    # select_ink = [select_ink, select_ink]
    # select_bg=cv2.imresize(bg[int(random()*num_bg)],w,h)
    _, thresh1 = cv2.threshold(orig, 127, 255, cv2.THRESH_BINARY)
    # ink + file +bg
    index = np.where(thresh1 == 0)
    orig[index] = select_ink[index] * 0.6
    threshold = random.randint(120, 200)
    _, thresh1 = cv2.threshold(orig, threshold, 255, cv2.THRESH_BINARY)
    orig[np.where(thresh1 == 255)] = select_bg[np.where(thresh1 == 255)]
    # add seal (to do)

    # crop
    shift_y, shift_x = abs((h - h_o)) // 2, abs((w - w_o)) // 2
    final = orig[shift_y:shift_y + h, shift_x:w - shift_x, :]
    mask = mask[shift_y:shift_y + h, shift_x:w - shift_x, :]
    ##
    # name=name[:-4]+'_2.txt'
    print(os.path.join(rootdir, 'scan_no_rotate', name.replace('jpg', 'jpg')))
    # cv2.imwrite(os.path.join(rootdir, 'scan_no_rotate', name.replace('jpg', 'jpg')), final)
    cv2.imshow('final', final)
    # cv2.imshow('mask', mask*255)
    # cv2.imshow('image', final*mask)
    cv2.waitKey()
# cv2.imwrite(os.path.join(rootdir,'scan_no_rotate_mask',name.replace('jpg','jpg')),mask)
## rotate bbox and save
# im=cv2.imread(os.path.join(rootdir,'image',name))
# h,w=final.shape
# with open(os.path.join(path),'r') as f:
# 	line=f.readline()
# 	cnt_box=line.strip('/n')
# 	line=f.readline()
# 	bbox=[]
# 	while line:
# 		tmp=line.rstrip('/n').split(' ')
# 		clas=tmp[4]
# 		[x0,y0,x1,y1]=list(map(int,tmp[0:4]))  # x0,y0,x1,y2
# 		box=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
# 		center_x,center_y=(w)/2.0,(h)/2.0
# 		line=f.readline()
# 		new_box=[]
# 		for loc in box:
# 			[x,y]=loc
# 			new_x=(x-center_x)*math.cos(theta)-(y-center_y)*math.sin(theta)+center_x
# 			new_y=(x-center_x)*math.sin(theta)+(y-center_y)*math.cos(theta)+center_y
# 			new_box.append(int(new_x))
# 			new_box.append(int(new_y))
# 		new_box.append(clas)
# 		bbox.append(new_box)
# with open(os.path.join(rootdir,'Textfile_revised',name),'w') as f:
# 	f.write(str(alpha)+'\n')
# 	# f.write(str(h)+' '+str(w)+'\n')
# 	for box in bbox:
# 		info=' '.join(map(str,box))
# 		f.write(info)
# 		f.write('\n')
# makexml(bbox)
