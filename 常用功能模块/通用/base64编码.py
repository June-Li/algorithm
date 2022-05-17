import base64
import cv2
import requests
import json

img_ori = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/my_imgs_11/0.jpg')

img = base64.b64encode(cv2.imencode(".jpg", img_ori.copy())[1].tobytes()).decode('utf8')
temp_img = img_ori.copy()
# request_url = args.tencent_ip
request_url = "http://106.55.81.17:60007/youtu/ocrapi/tableocr"
# request_url = "http://25.66.138.153:60007/youtu/ocrapi/tableocr"
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
print(response['tableRes'])
print()
