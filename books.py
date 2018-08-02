import requests
from bs4 import BeautifulSoup
import re 
import time
import os
import sys

def books_url(ranges):
    bookurls = []
    urls = 'https://www.xuanhuanwu.com/xhw'
    for i in range(ranges,ranges+1):           
        bookurl_one = ''.join([urls,str(i)]) 
        bookurls.append(bookurl_one)
    return bookurls

def one_book_url(bookurls):
    one_bookurl = []
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
            }
    for bookurl in bookurls:
        nover = requests.get(bookurl,headers = headers)
        if nover.ok and len(nover.text) > 8000:
            None
        else:
            print('请求失败: ' + bookurl)   
            pass
        soup = BeautifulSoup(nover.text,"lxml")
        bookname = soup.title.string
        patten = re.compile('<dd> <a style="" href="(.*?)">')
        patten2 = re.compile('_(.*?)无弹窗_')
        #提取链接正则
        urls = re.findall(patten,nover.text)
        bookname = re.findall(patten2,bookname)
        #正则提取
        string = ''.join([bookname[0],'.txt'])
        for i in urls:
            one_bookurl.append('https://www.xuanhuanwu.com' + i)
        one_bookurl.append(string)
    return one_bookurl
        #返回书籍章节链接

def book_down(one_bookurl):
    zao = time.time()
    headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
                }
    zhanngjie=str(len(one_bookurl)-1)
    print(one_bookurl[-1][:-4] + ' : 共' +zhanngjie +  '章' + '正在下载...')
    for i in one_bookurl[:-2]:    
        one_paper = requests.get(i,headers = headers)
        if one_paper.status_code == 200:
            soup = BeautifulSoup(one_paper.text,'lxml')
            title = soup.h1.string
            dd = str(soup.find_all(id = 'content'))
            #粗剪正文
            dd = '\n\n' + title + '\n\n' + dd[61:-47]
            strs = re.sub('<br/><br/>', '\n', dd)
            #细剪正文
            with open(one_bookurl[-1],'a',encoding= 'utf-8')as f:
                f.write(strs)
            #存入一章
        else:
            print('请求失败: ' + i)
    print(one_bookurl[-1][:-4] + ' 下载完成')
    wan = time.time()
    yongshi = str(wan - zao)
    file = os.getcwd()
    print('文件在:' + file)
    print('用时: ' + yongshi[:5] + '秒')

def down(ranges):
    #ranges = int(input('输入玄幻屋的书号:'))
    book_down(one_book_url(books_url(ranges)))