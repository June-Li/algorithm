import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64

try:
    cred = credential.Credential("", "")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

    req = models.SealOCRRequest()
    f = open('/Volumes/my_disk/company/sensedeal/dataset/印章/v1/images/train/baidu_fapiao_12.jpg', 'rb')
    img = base64.b64encode(f.read()).decode('utf8')
    params = {
        "ImageBase64": img
    }
    req.from_json_string(json.dumps(params))

    resp = client.SealOCR(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
