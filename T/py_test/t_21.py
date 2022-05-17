import re
from bs4 import BeautifulSoup


def bs4_paraser(html):
    all_value = []
    value = {}
    soup = BeautifulSoup(html, 'html.parser')
    # 获取影评的部分
    # all_div = soup.find_all('div', attrs={'class': 'yingping-list-wrap'}, limit=1)
    all_div = soup.find_all('div', limit=1)
    for row in all_div:
        # 获取每一个影评，即影评的item
        all_div_item = row.find_all('div', attrs={'class': 'item'})
        for r in all_div_item:
            # 获取影评的标题部分
            title = r.find_all('div', attrs={'class': 'g-clear title-wrap'}, limit=1)
            if title is not None and len(title) > 0:
                value['title'] = title[0].a.string
                value['title_href'] = title[0].a['href']
                score_text = title[0].div.span.span['style']
                score_text = re.search(r'\d+', score_text).group()
                value['score'] = int(score_text) / 20
                # 时间
                value['time'] = title[0].div.find_all('span', attrs={'class': 'time'})[0].string
                # 多少人喜欢
                value['people'] = int(
                    re.search(r'\d+', title[0].find_all('div', attrs={'class': 'num'})[0].span.string).group())
            # print r
            all_value.append(value)
            value = {}
    return all_value


base_path = '/root/bbtv/MyLearn/algorithm/T/html_test/t_3.html'
# lines = open(base_path, 'r').readlines()
# html = ''
# for line in lines:
#     html += line
out = bs4_paraser(open(base_path))
print(out)

