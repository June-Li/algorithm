import cv2
import imageio
import os
import numpy as np

# def read_image(image_path):
#     image_name_list = os.listdir(image_path)
#     frame_count = 0
#     all_frames = []
#     for image_name in image_name_list:
#         frame = cv2.imread(image_path + image_name)
#         all_frames.append(frame)
#         cv2.imshow('frame', frame)
#         cv2.waitKey(1)
#         frame_count += 1
#         print(frame_count)
#     print('===>', len(all_frames))
#
#     return all_frames
#
#
# def frame_to_gif(frame_list):
#     gif = imageio.mimsave('/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/result.gif', frame_list, 'GIF')
#
#
# if __name__ == "__main__":
#     frame_list = read_image('/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/output/')
#     frame_to_gif(frame_list)


h, w, _ = np.shape(cv2.imread('/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/output/000000.png'))

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/result.avi', fourcc, 5.0, (w, h), True)

fps = 5
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter()
out.open('/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/result.mp4', fourcc, fps, (w, h), True)

image_path = '/Volumes/my_disk/备份Work/SANY/PyTorch-YOLOv3-send/output/'
image_name_list = os.listdir(image_path)

for image_name in image_name_list:
    frame = cv2.imread(image_path + image_name)
    # cv2.imshow('frame', frame)
    out.write(frame)
    # cv2.waitKey(1)

out.release()
cv2.destroyAllWindows()
