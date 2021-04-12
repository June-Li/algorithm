import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
import numpy as np
import urllib.request
import cv2

try:
    cred = credential.Credential("AKIDmMi4FC5PH0VlIcEreleIhtPjlYKtsC0s", "Zu1FExRzLV8XhIfmhdKoBJMDovGLBk3t")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

    req = models.RecognizeTableOCRRequest()
    # params = {
    #     "ImageUrl": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Foss.gkstk.com%2Fimages%2F2016%2F1%2F20160130101540437.jpeg&refer=http%3A%2F%2Foss.gkstk.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1619080078&t=cfa59e14c86cb64f80f812cf538a2ea4"
    # }
    # f = open("/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/37.jpg", "rb")
    # base64data = base64.b64encode(f.read())  # 得到 byte 编码的数据
    # base64data = str(base64data, 'utf-8')  # 重新编码数据
    # params = {"ImageBase64": "' + base64data + '"}

    lines = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/37.txt', 'r').readlines()
    for index, url in enumerate(lines):
        # url = "http://m.qpic.cn/psc?/V519xkby2jxUud3BokKM1jiJVJ4RAg7W/TmEUgtj9EK6.7V8ajmQrEBa5VdOquUQOxg73IsZ8OaXBoPhaIGkcl2vKYg6.U94Zo5P.OWypKtGexn3OG6ta51YCXO6RzoEMSN5Ui2czkIY!/b&bo=oAU4BKAFOAQBKQ4!&rf=viewer_4&t=5"
        params = {
            "ImageUrl": url
            # "ImageBase64": "/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/37.txt"
        }
        req.from_json_string(json.dumps(params))

        resp = client.RecognizeTableOCR(req)
        resp_json = resp.to_json_string()
        f = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/out_img/' + str(index) + '.json', 'w')
        json.dump(resp_json, f)
        resp_dict = json.loads(resp_json)

        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # image = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/37.jpg')
        txt_out = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/out_img/' + str(index) + '.txt', 'a+')
        for table in resp_dict['TableDetections']:
            cells = table['Cells']
            # cells = resp_dict['TableDetections'][0]
            if cells[0]['ColTl'] != -1:
                txt_out.write('<table>\n')
                for cell in cells:
                    x_0, y_0, x_1, y_1 = cell['Polygon'][0]['X'], cell['Polygon'][0]['Y'], cell['Polygon'][2]['X'], cell['Polygon'][2]['Y']
                    cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), 2)
                    txt_out.write(str(cell['RowTl']) + ',' + str(cell['ColTl']) + ',' + str(cell['RowBr']) + ',' + str(cell['ColBr']) + '|' + cell['Text'] + '\n')
                txt_out.write('</table>\n')
            else:
                for cell in cells:
                    x_0, y_0, x_1, y_1 = cell['Polygon'][0]['X'], cell['Polygon'][0]['Y'], cell['Polygon'][2]['X'], cell['Polygon'][2]['Y']
                    cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), 2)
                    txt_out.write(cell['Text'] + '\n')
        # cv2.namedWindow('image', 0)
        txt_out.close()
        cv2.imwrite('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/out_img/' + str(index) + '.jpg', image)
        # cv2.imshow('image', image)
        # cv2.waitKey()

        # print(resp_json)
        print('processed num: ', index)

except TencentCloudSDKException as err:
    print(err)
