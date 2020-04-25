#encoding:utf-8
#author:simple
import requests
from fake_useragent import UserAgent
from lxml import etree
import re
ua = UserAgent()
# etree = html.etree
headers = ua.random
# url = 'https://www.zoomoffices.com/h-pr-j-3_{0}.html#pcp={0}'
start_urls = 'https://www.zoomoffices.com/h-pr-j-3_{0}.html?complexStaticUrl=true&m22pageno={1}#module22'
headers = {'User-Agent': headers}
# page_url = 'https://www.zoomoffices.com/h-pr-j-3_{0}.html?complexStaticUrl=true&m22pageno={1}#module22'

# 传统办公url
p_url ='https://www.zoomoffices.com/h-pr.html?pfc=%257B%2522groupIds%2522%253A%255B%s%255D%252C%2522lid%2522%253A3%257D#module22'


def get_city(url):

    data = requests.get(url, headers=headers)
    html = etree.HTML(data.text)
    # print(html)
    detail_urls = html.xpath('//div[@class="propList  "]/table/tr/td/a/@href')
    # print(detail_urls)
    for url in detail_urls:
        detail_url = 'https://www.zoomoffices.com/' + url.split("#")[0]
        # print(detail_url)
        detail_page(detail_url)
    next_page = html.xpath('//a[@class="sortPageNext1"]/@href')
    if next_page:
        next_url = 'https://www.zoomoffices.com/' + next_page[0]
        get_city(next_url)
    else:
        pass
    # print(html)
    title = html.xpath('//table/tbody[2]/tr/td/a/@href')
    # print(title)
    # selector = html.fromstring(data.text)
    # detail_urls = selector.xpath('//tbody/tr/td/a/text()')
    # us = re.findall('<a hidefocus="true" href="(.*) target="_blank"', data.text, re.S)
    # soup = BeautifulSoup(data.text, 'lxml')
    # us = soup.find_all('.propDiv')
    # print(detail_urls)
    # print(selector)
    # print(data.text)
ll = []
def detail_page(url):
    data = requests.get(url, headers=headers)
    print(data.status_code)
    print(data.url)
    ll.append(data.url)




# for i in range(1, 50):
#
#     data = requests.get(page_url.format(14, i), headers=headers)
#     print(data.status_code)



if __name__ == '__main__':

    city_dic = {'北京': '14', '上海': '1', '深圳': '17', '广州': '15'}
    for v in city_dic.values():
        get_city(start_urls.format(v, 1))

    print(ll)