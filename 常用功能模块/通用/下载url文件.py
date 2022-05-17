import os
import requests


def download(url, out_path, log_file):
    filename = url.split('/')[-1]

    try:
        req = requests.get(url)
        if req.status_code != 200:
            print('下载异常: ', url)
            log_file.write(url + '\n')
            return
        with open(out_path + filename, 'wb') as f:
            f.write(req.content)
            print('下载成功: ', url)
    except Exception as e:
        print(e)
        log_file.write(str(e) + url + '\n')


if __name__ == '__main__':
    out_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/pdf/'
    exit_list = os.listdir(out_path)
    log_file = open('/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/error.txt', 'w')
    lines = open('/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/filter_pdf_list.txt', 'r').readlines()
    for count, line in enumerate(lines):
        url = line.strip('\n')
        if url.split('/')[-1] in exit_list:
            continue
        download(url, out_path, log_file)
        if count % 100 == 0:
            print('processed num: ', count + 1)
