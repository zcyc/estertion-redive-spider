from bs4 import BeautifulSoup
import requests


# 此处的url是调用的时候传进来的
def get_company_detail(url):
    # 获取网页源码
    res_body = requests.get(url)
    # 格式化成bs数据
    html = BeautifulSoup(res_body.text, features="html.parser")
    # 找到所有的表格的行
    content = html.findAll('tr')
    # 设置一个变量存储数据
    regis_info = []
    # 设置一个条件用来跳过第一个表格
    x = 0
    # 循环刚才网页中的数据
    for i in range(0, len(content)):
        # 如果发现第二张表的表头则把x设置成1，开始储存数据
        if "Player" in content[i].get_text():
            x = 1
        # 如果是第二张表的数据就存起来
        if x == 1:
            data = content[i].get_text().replace("\n\n", "\n")
            regis_info.append(data)
            i = i + 1
    # 打印前10条数据，第0条是表头
    print(regis_info[1])


# 这是要获取的网页的链接
get_company_detail("https://asia.wows-numbers.com/zh-tw/ship/4276041424,Yamato/")
