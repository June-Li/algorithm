# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_ocr20191230.client import Client as ocr20191230Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr20191230 import models as ocr_20191230_models
from viapi.fileutils import FileUtils

file_utils = FileUtils('LTAI5tBRL5zZF259pCaxVoiH', 'QAMNpGYuLGKGtRzSQfNUR6sX5TwMw9')
base_path = '/root/bbtv/MyLearn/algorithm/DATASETS/印章/v0/'
image_name = "1209712058_16.jpg"
suffix = image_name[::-1].split('.', 1)[0][::-1]
oss_url = file_utils.get_oss_url(base_path + image_name, suffix, True)
# oss_url = file_utils.get_oss_url('https://img2.baidu.com/it/u=2580411447,210980984&fm=26&fmt=auto&gp=0.jpg', 'jpg', False)
print(oss_url)


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> ocr20191230Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'ocr.cn-shanghai.aliyuncs.com'
        return ocr20191230Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client('LTAI5tBRL5zZF259pCaxVoiH', 'QAMNpGYuLGKGtRzSQfNUR6sX5TwMw9')
        recognize_stamp_request = ocr_20191230_models.RecognizeStampRequest(
            image_url=oss_url
        )
        # 复制代码运行请自行打印 API 的返回值
        out = client.recognize_stamp(recognize_stamp_request)
        print(out)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        recognize_stamp_request = ocr_20191230_models.RecognizeStampRequest(
            image_url=oss_url
        )
        # 复制代码运行请自行打印 API 的返回值
        await client.recognize_stamp_async(recognize_stamp_request)


if __name__ == '__main__':
    Sample.main([])
