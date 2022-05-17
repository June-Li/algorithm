import os
import shutil


base_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/images/'
out_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/images_split/'
image_name_list = os.listdir(base_path)
for idx, image_name in enumerate(image_name_list):
    file_name = idx // 10000
    out_file = out_path + str(file_name) + '/'
    if not os.path.exists(out_file):
        os.makedirs(out_file)
    shutil.move(base_path + image_name, out_file + image_name)
    print('processed num: ', idx)

