from urllib import request
import gzip
import re


respone = request.urlopen('https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1620294053495_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E7%AB%A0%E7%A8%8B%E7%9B%96%E7%AB%A0')
# respone = request.urlopen('http://www.qq.com')
html = respone.read()

# try:
#     html = gzip.decompress(html)
# except:
#     pass
#
# try:
#     html = html.decode('utf-8')
# except:
#     html = html.decode('gbk')

# html = gzip.decompress(html)
html = html.decode('utf-8')
print(html)

reg = 'src="(.+?)" lazy'
imgre = re.compile(reg)
image_list = imgre.findall(html)
print('******************************')
print(image_list)

for index, image_url in enumerate(image_list):
    request.urlretrieve(image_url, './out/' + str(index) + '.jpg')
