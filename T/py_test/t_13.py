# import imageio
# import cv2
# import os
#
#
# def read_image(image_path):
#     image_name_list = os.listdir(image_path)
#     frame_count = 0
#     all_frames = []
#     for image_name in image_name_list:
#         frame = cv2.imread(image_path + image_name)
#         all_frames.append(frame)
#         cv2.imshow('frame', frame)
#         cv2.waitKey()
#         frame_count += 1
#         print(frame_count)
#     print('===>', len(all_frames))
#
#     return all_frames
#
#
# def frame_to_gif(frame_list):
#     gif = imageio.mimsave('./result.gif', frame_list, 'GIF')
#
#
# if __name__ == "__main__":
#     frame_list = read_image('./out/')
#     frame_to_gif(frame_list)

import base64
import cv2
import requests
import json

img_ori = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/my_imgs_11/0.jpg')

img = base64.b64encode(cv2.imencode(".jpg", img_ori.copy())[1].tobytes()).decode('utf8')
temp_img = img_ori.copy()
# request_url = args.tencent_ip
request_url = "http://106.55.81.17:60007/youtu/ocrapi/tableocr"
params = {"app_id": '123456', "image": img,
          "options": {"preprocess": True,
                      "enable_ret_excel": True,
                      "side_detect_short": 20,
                      "side_detect_long": 3500}}

headers = {'Host': '<calculated when request is sent>',
           'Content-type': 'application/json',
           'Content-Length': '<calculated when request is sent>'}
response = requests.post(request_url, data=json.dumps(params), headers=headers)
response.encoding = 'utf-8'
response = json.loads(response.text)
print()