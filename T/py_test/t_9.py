from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests


def getnamepage(name):
    b.get('https://pic.sogou.com/pics?query=%E5%8F%91%E7%A5%A8&w=05009900')
    # search_box = b.find_element_by_id('kw')
    # search_box.send_keys(name)
    # search_box.send_keys(Keys.ENTER)
    # time.sleep(5)


def download(imglist, num):
    # 选取大尺寸
    # ele = b.find_element_by_id('sizeFilter')
    # ActionChains(b).move_to_element(ele).perform()
    # time.sleep(5)
    # ele4 = b.find_element_by_xpath('//*[@id="sizeFilter"]/div/ul/li[3]')
    # ActionChains(b).move_to_element(ele4).perform()
    # time.sleep(5)
    # ele4.click()
    # time.sleep(5)

    # 打开第一张图片，在此界面中点击左右切换图片
    ele1 = b.find_element_by_xpath('//*[@id="videoApp"]/div/div[2]/div/ul/li[1]/div/a[1]/img')
    ele1.click()
    b.switch_to.window(b.window_handles[1])  # 很重要的一步，切换窗口，否则页面找不到元素,python shell里面是b.switch_to_window
    x = 1
    for i in range(1, num + 1):
        print('processed num: ', i)
        # ele3=b.find_element_by_xpath('/html/body/div[1]/div[2]/div/span[2]/span')
        # ele3.click()
        # time.sleep(3)#为保险起见，设置一个睡眠和爬取的时间差
        ele2 = b.find_element_by_xpath('//*[@id="imgArea"]/div[3]/div/div/a/img')
        img = ele2.get_attribute('src')  # 获取当前图片的url链接
        r = requests.get(img)
        if r.status_code == 200:
            path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl/发票盖章/%d.jpg' % x
            print('正在爬取  ' + img)
            with open(path, 'wb') as f:
                f.write(r.content)
                time.sleep(1)
                f.close()
                print('爬取成功')
                x += 1
            ele3 = b.find_element_by_xpath('//*[@id="imgArea"]/a[2]/span')
            ele3.click()
            # time.sleep(3)
        # 跳到下一张
        else:
            ele3 = b.find_element_by_xpath('//*[@id="imgArea"]/a[2]/span')
            ele3.click()
            time.sleep(1)
            continue



if __name__ == "__main__":
    b = webdriver.Chrome()
    name = '发票'  # 定义要搜索的内容
    num = 500
    imglist = []
    getnamepage(name)
    download(imglist, num)
    b.close()
