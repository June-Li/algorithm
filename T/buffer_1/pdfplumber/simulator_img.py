### Simulate scanned file from PDF file
### Written by Yuhsuan 2018.11.23
import os
import cv2

import random
import numpy as np
import skimage
def noise(image):
	temp_image = np.float64(np.copy(image))
	h = temp_image.shape[0]
	w = temp_image.shape[1]
	noise = np.random.randn(h, w) * 35
	noisy_image = np.zeros(temp_image.shape, np.float64)
	if len(temp_image.shape) == 2:
		noisy_image = temp_image + noise
	else:
		noisy_image[:,:,0] = temp_image[:,:,0] + noise
		noisy_image[:,:,1] = temp_image[:,:,1] + noise
		noisy_image[:,:,2] = temp_image[:,:,2] + noise

	return noisy_image

def rotate(img):

	return img

def sharp(img):
	kernel = np.array([[1,1,1], [1,-7,1], [1,1,1]])
	img = cv2.filter2D(img, -1, kernel)
	return img

def seal(img):

	return img

def main():
	dirname='/home/sxs/yuhsuan/data/personal/JPEGImages'
	savepath='/home/sxs/yuhsuan/data/personal_simu/JPEGImages'
	filelist=os.listdir(dirname)

	for file in filelist:
		image=cv2.imread(os.path.join(dirname,file))
		index_noise = random.randint(0, 10)*0.1
		# image=noise(image)
		# if index_noise>0.5:
		# 	image=noise(image)
		# 	index_noise = random.randint(0, 10)*0.1
		# if index_noise>0.2:
		# 	image=rotate(image)
		# 	index_noise = random.randint(0, 10)*0.1
		# if index_noise>0.3:
		# 	image=sharp(image)
		# 	index_noise = random.randint(0, 10)*0.1
		# if index_noise>0.8:
		# 	image=seal(image)

		cv2.imwrite(os.path.join(savepath,file),image)

if __name__ == "__main__":
	main()