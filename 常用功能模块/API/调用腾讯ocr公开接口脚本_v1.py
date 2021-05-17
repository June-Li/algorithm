import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
import numpy as np
import cv2
import os


try:
    cred = credential.Credential("AKIDmMi4FC5PH0VlIcEreleIhtPjlYKtsC0s", "Zu1FExRzLV8XhIfmhdKoBJMDovGLBk3t")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

    req = models.RecognizeTableOCRRequest()

    image_root_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/my_imgs_11/'
    image_name_list = os.listdir(image_root_path)

    # lines = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/img_list.txt', 'r').readlines()
    for index, image_name in enumerate(image_name_list):
        f = open(image_root_path + image_name, 'rb')
        img = base64.b64encode(f.read()).decode('utf8')
        params = {
            "ImageBase64": img
        }
        req.from_json_string(json.dumps(params))

        resp = client.RecognizeTableOCR(req)
        resp_json = resp.to_json_string()
        f = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/tencent_out/struct/' + str(index) + '.json', 'w')
        json.dump(resp_json, f)
        resp_dict = json.loads(resp_json)

        image = cv2.imread(image_root_path + image_name)
        # cv2.imwrite('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/tencent_out/images/' + str(index) + '.jpg', image)
        img_h, img_w, _ = np.shape(image)

        # image = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/37.jpg')
        txt_out = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/tencent_out/struct/' + str(index) + '_struct.txt', 'a+')
        box_out = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/tencent_out/labels/' + str(index) + '.txt', 'a+')
        for table in resp_dict['TableDetections']:
            cells = table['Cells']
            # cells = resp_dict['TableDetections'][0]
            if cells[0]['ColTl'] != -1:
                txt_out.write('<table>\n')
                for cell in cells:
                    x_0, y_0, x_1, y_1 = cell['Polygon'][0]['X'], cell['Polygon'][0]['Y'], cell['Polygon'][2]['X'], cell['Polygon'][2]['Y']
                    cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), 2)
                    txt_out.write(str(cell['RowTl']) + ',' + str(cell['ColTl']) + ',' + str(cell['RowBr']) + ',' + str(cell['ColBr']) + '|' + cell['Text'] + '\n')
                    # 输出yolo格式的box-开始
                    x_center, y_center, w, h = (x_0 + x_1) / 2 / img_w, (y_0 + y_1) / 2 / img_h, abs(x_0 - x_1) / img_w, abs(y_0 - y_1) / img_h
                    box_out.write(' '.join(['0', str(x_center), str(y_center), str(w), str(h) + '\n']))
                    # 输出yolo格式的box-结束
                txt_out.write('</table>\n')
            else:
                for cell in cells:
                    x_0, y_0, x_1, y_1 = cell['Polygon'][0]['X'], cell['Polygon'][0]['Y'], cell['Polygon'][2]['X'], cell['Polygon'][2]['Y']
                    cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), 2)
                    txt_out.write(cell['Text'] + '\n')
        txt_out.close()
        box_out.close()
        cv2.imwrite('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/tencent_out/show/' + str(index) + '.jpg', image)
        # cv2.imshow('image', image)
        # cv2.waitKey()

        print('processed num: ', index)

except TencentCloudSDKException as err:
    print(err)
