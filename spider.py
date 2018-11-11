import requests
import os
import time
import pandas as pd
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
                  'BIDUBrowser/8.7 Safari/537.36 '
}


def catchHouseList(url):
    resp = requests.get(url, headers=headers, stream=True)
    if resp.status_code == 200:
        reg = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
        urls = re.findall(reg, resp.text)
        return urls
    return []


def catchHouseDetail(url):
    resp = requests.get(url, headers=headers)
    print(url)
    if resp.status_code == 200:
        info = {}
        soup = BeautifulSoup(resp.text, 'html.parser')
        info['标题'] = soup.select('.main')[0].text
        info['总价'] = soup.select('.total')[0].text
        info['总价单位'] = soup.select('.unit')[0].text
        info['每平方售价'] = soup.select('.unitPriceValue')[0].text
        # p = soup.select('.tax')
        # info['参考总价'] = soup.select('.tax')[0].text
        info['建造时间'] = soup.select('.subInfo')[2].text
        info['小区名称'] = soup.select('.info')[0].text
        info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
        info['链家编号'] = str(url)[34:].rsplit('.html')[0]
        info['房屋户型'] = str(soup.select('.content')[2].select('.label')[0].next_sibling)
        info['所在楼层'] = soup.select('.content')[2].select('.label')[1].next_sibling
        info['建筑面积'] = soup.select('.content')[2].select('.label')[2].next_sibling
        info['户型结构'] = soup.select('.content')[2].select('.label')[3].next_sibling
        info['套内面积'] = soup.select('.content')[2].select('.label')[4].next_sibling
        info['建筑类型'] = soup.select('.content')[2].select('.label')[5].next_sibling
        info['房屋朝向'] = soup.select('.content')[2].select('.label')[6].next_sibling
        info['建筑结构'] = soup.select('.content')[2].select('.label')[7].next_sibling
        info['装修情况'] = soup.select('.content')[2].select('.label')[8].next_sibling
        info['梯户比例'] = soup.select('.content')[2].select('.label')[9].next_sibling
        info['供暖方式'] = soup.select('.content')[2].select('.label')[10].next_sibling
        info['配备电梯'] = soup.select('.content')[2].select('.label')[11].next_sibling
        return info
    pass


def appendToXlsx(info):
    fileName = '链家二手房.xlsx'
    dfNew = pd.DataFrame([info])
    if (os.path.exists(fileName)):
        sheet = pd.read_excel(fileName)
        dfOld = pd.DataFrame(sheet)
        df = pd.concat([dfOld, dfNew])
        df.to_excel(fileName)
    else:
        dfNew.to_excel(fileName)


def catch():
    pages = ['https://sz.lianjia.com/ershoufang/pg{}/'.format(x) for x in range(1, 101)]
    for page in pages:
        print(page)
        houseListURLs = catchHouseList(page)
        for houseDetailUrl in houseListURLs:
            try:
                info = catchHouseDetail(houseDetailUrl)
                appendToXlsx(info)
            except:
                pass
            time.sleep(3)

    pass


if __name__ == '__main__':
    catch()
