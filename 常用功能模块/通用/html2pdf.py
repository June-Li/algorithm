# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 10:49
# @Author  : lijun
# 环境配置教程：https://blog.csdn.net/weixin_38640670/article/details/120524976
import pdfkit
import os
import re


def rectify_charset(html, charset='utf-8'):
    if '<meta charset=' in html:
        re.sub(r'<meta charset=(.*?)>', '<meta charset=\'' + charset + '\'>', html)
    else:
        if '<head>' in html and '</head>' in html:
            re.sub(r'<head>', '<head>\n<meta charset=\'' + charset + '\'>\n', html)
        else:
            html = '<head>\n<meta charset=\'' + charset + '\'>\n</head>\n' + html
    return html


def main():
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "utf-8",
        'custom-header': [('Accept-Encoding', 'gzip')],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None
    }

    base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/a/20220411/show/'
    in_html_name_list = os.listdir(base_path)
    # out_path = '/Users/lijun/Downloads/'
    out_path = base_path.replace('/show/', '/show_pdf/')

    for idx, html_name in enumerate(in_html_name_list):
        # pdfkit.from_file(
        #     base_path + '/test_data/my_html_0/' + html_name,
        #     out_path + html_name[::-1].split('.', 1)[-1][::-1] + '.pdf',
        #     options=options)
        if not html_name.endswith('.html'):
            continue

        html = ''.join(open(base_path + html_name, 'r', encoding='utf-8').readlines())
        # html = rectify_charset(html, 'utf-8')
        pdfkit.from_string(
            html,
            out_path + html_name[::-1].split('.', 1)[-1][::-1] + '.pdf',
            options=options)

        # pdfkit.from_string(
        #     'hello',
        #     out_path + html_name[::-1].split('.', 1)[-1][::-1] + '.pdf',
        #     options=options)

        print('current processed num: ', idx + 1)


if __name__ == '__main__':
    main()
