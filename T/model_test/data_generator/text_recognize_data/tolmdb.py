import os
import lmdb  # install lmdb by "pip install lmdb"
import cv2
import re
from PIL import Image
import numpy as np
import imghdr
import random


def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    try:
        imageBuf = np.fromstring(imageBin, dtype=np.uint8)
        img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
        imgH, imgW = img.shape[0], img.shape[1]
    except:
        return False
    else:
        if imgH * imgW == 0:
            return False
    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k, v)


def createDataset(outputPath, imagePathList, labelList, imagePathList2, lexiconList=None, checkValid=True):
    """
    Create LMDB dataset for CRNN training.
    ARGS:
        outputPath    : LMDB output path
        imagePathList : list of image path
        labelList     : list of corresponding groundtruth texts
        lexiconList   : (optional) list of lexicon lists
        checkValid    : if true, check the validity of every image
    """
    assert (len(imagePathList)+len(imagePathList2) == len(labelList))
    nSamples = len(labelList)
    env = lmdb.open(outputPath, map_size=1099511627776)
    cache = {}
    cnt = 1
    for i in range(nSamples):
        if i < len(imagePathList):
            tmp = imagePathList[i].split()[0]
            imagePath = '/home/sxs/djy/ocr/dataset/crnn/generator_img/' + tmp.split('/')[-1]
        # print(imagePath)
            label = ''.join(labelList[i])
            #print(label)
        else:
            tmp = imagePathList2[i-len(imagePathList)].split()[0]
            imagePath = '/home/sxs/djy/images/' + tmp
            label = ''.join(labelList[i])
            #print(label)
        # if not os.path.exists(imagePath):
        #     print('%s does not exist' % imagePath)
        #     continue

        with open(imagePath, 'r') as f:
            imageBin = f.read()

        if checkValid:
            if not checkImageIsValid(imageBin):
                print('%s is not a valid image' % imagePath)
                continue
        imageKey = 'image-%09d' % cnt
        labelKey = 'label-%09d' % cnt
        cache[imageKey] = imageBin
        cache[labelKey] = label
        if lexiconList:
            lexiconKey = 'lexicon-%09d' % cnt
            cache[lexiconKey] = ' '.join(lexiconList[i])
        if cnt % 1000 == 0:
            writeCache(env, cache)
            cache = {}
            print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
        print(cnt)
    nSamples = cnt - 1
    cache['num-samples'] = str(nSamples)
    writeCache(env, cache)
    print('Created dataset with %d samples' % nSamples)


if __name__ == '__main__':
    outputPath = "/home/sxs/djy/ocr/dataset/crnn/train0111"
    imgdata = open("/home/sxs/djy/ocr/data_generator/text_recognize_data/train.txt")
    imagePathList = list(imgdata)
    imgdata2 = open('/home/sxs/djy/data/train.txt')
    imagePathList2 = random.sample(list(imgdata2), 500000)
    labelList = []
    label2 = list(open('/home/sxs/djy/ocr/dataset/crnn/char_std_5991.txt'))
    label = []
    for line in label2:
        line = line.strip('\r')
        line = line.strip('\n')
        label.append(line)
    with open('label.txt', 'w') as f:
        f.write(''.join(label))
    for line in imagePathList:
        word = line.split()[1]
        labelList.append(word)
    for line in imagePathList2:
        line = line.strip('\r')
        line = line.strip('\n')
        arr = line.split()
        word = ''
        for s in arr[1:]:
            word += label[int(s)]
        labelList.append(word)
    createDataset(outputPath, imagePathList, labelList, imagePathList2)
