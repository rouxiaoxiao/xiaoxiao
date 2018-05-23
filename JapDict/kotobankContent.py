# -*-coding:utf-8-*-
# import urllib
import json
import random
import sys
import time
import urllib
import urllib2

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
import cookielib

headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]


# https://zh.wiktionary.org/wiki/%E5%A5%BD
def get_content(url):
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "kotobank.jp")
    req.add_header("Referer", "https://kotobank.jp/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        # time.sleep(2)
        soup = BeautifulSoup(content, "lxml")
        # 定义返回的json字符串
        JapWords = {}
        # 获取词头
        if (soup.select('h1')[0].find('span')):
            pianJiaMing = soup.select('h1')[0].find('span').get_text().strip().replace("\n", "")
            wordHead = soup.select('h1')[0].get_text().replace(pianJiaMing, '').strip().replace("\n", "")
            JapWords['pianJiaMing'] = pianJiaMing
        else:
            wordHead = soup.select('h1')[0].get_text().strip().replace("\n", "")
        JapWords['wordHead'] = wordHead
        # 获取读音
        # 获取日语简明释义
        matas = soup.find_all('meta')
        print(matas)
        jianmingshiyi = ""
        for meta in matas:
            if (meta.get('name') == 'description'):
                print("jianmingshiyi:" + meta.get('content'))
            # print(meta[''])
            # if (meta['name']=="description"):
            #     jianmingshiyi=meta['content']
        # 各本书中的释义
        size = len(soup.find_all('article'))
        tansCn_list = []
        for i in range(0, size):
            tranCn = {}
            # 书籍名称
            article = soup.find_all('article')[i]
            bookName = article.find('h2').get_text().replace(' ', '').strip().replace("\n", "")
            # 该书中的平假名
            if (article.find('h3')):
                pingJiaMing = article.find('h3').get_text().replace(' ', '').strip().replace("\n", "")
                tranCn['pingJiaMing'] = pingJiaMing
            # 该书中的释义
            if (soup.findAll('section')[i]):
                section = soup.findAll('section')[i].get_text().replace(' ', '').strip().replace("\n", "")
                tranCn['description'] = section
            tranCn['bookName'] = bookName
            tansCn_list.append(tranCn)
            print(bookName + ' ' + pingJiaMing + ' ' + section)
        JapWords['transCns'] = tansCn_list
        JapWords['jianmingshiyi'] = jianmingshiyi
        return json.dumps(JapWords, encoding="UTF-8", ensure_ascii=False)
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    JapWord_file = open("C:\Users\liangxiaolx\Desktop\JapWordSpider\dataOut\JapWordDes.json", "a")
    url_data_file = open("C:\Users\liangxiaolx\Desktop\JapWordSpider\dataIn\wordHead.txt")
    i = 0
    for line in url_data_file:
        i = i + 1
        print('~~~~~我是第' + str(i) + '个单词~~~~~位于' + line.split("####")[0] + '~~~~~' + time.asctime(
            time.localtime(time.time())))
        url = line.split("####")[2].replace("\n", "")
        print(url)
        howlong = [0.1, 0.2, 0.3, 0.4]
        time.sleep(random.choice(howlong))
        # get_content(url)
        if get_content(url) != None:
            try:
                JapWord_file.write(get_content(url) + "\n")
            except TypeError, a:
                print a
    url_data_file.close()
    JapWord_file.close()
    url = 'https://kotobank.jp/word/%E3%81%82-420491'