import cv2
import numpy as np
import os


base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/table/'
in_images_path = base_path + '/together/images/'
in_labels_path = base_path + '/together/labels/'
out_images_path = base_path + '/cls/'
out_exit_file_list_t = os.listdir(out_images_path + '0') + os.listdir(out_images_path + '1') + os.listdir(out_images_path + '_')
out_exit_file_list = [i[::-1].split('_', 1)[-1][::-1] + '.jpg' for i in out_exit_file_list_t]
skip_list = ['total_5361_015.jpg', 'total_2_44.jpg']
image_name_list = os.listdir(in_images_path)
for count, image_name in enumerate(image_name_list):
    try:
        if image_name in out_exit_file_list or image_name in skip_list:
            continue
        print('current processe image name: ', image_name)
        image_path = in_images_path + image_name
        label_path = in_labels_path + image_name.replace('.jpg', '.txt')
        image = cv2.imread(image_path)
        cv2.imshow('image', image)
        label = open(label_path, 'r').readlines()
        for index, line in enumerate(label):
            line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
            [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
            x_0 = int((x_center - weight / 2) * np.shape(image)[1])
            y_0 = int((y_center - height / 2) * np.shape(image)[0])
            x_1 = int((x_center + weight / 2) * np.shape(image)[1])
            y_1 = int((y_center + height / 2) * np.shape(image)[0])
            table = image[y_0:y_1, x_0:x_1]
            cv2.imshow('tabel', table)
            key = cv2.waitKey()
            if key == ord('4'):
                cv2.imwrite(out_images_path + '0/' + image_name[::-1].split('.', 1)[-1][::-1] + '_' + str(index) + '.jpg', table)
            elif key == ord('6'):
                cv2.imwrite(out_images_path + '1/' + image_name[::-1].split('.', 1)[-1][::-1] + '_' + str(index) + '.jpg', table)
            else:
                cv2.imwrite(out_images_path + '_/' + image_name[::-1].split('.', 1)[-1][::-1] + '_' + str(index) + '.jpg', table)
    except:
        print('error processe image name: ', image_name)
    if count % 100 == 0:
        print('processed num: ', count)
