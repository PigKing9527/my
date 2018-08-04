# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup
import re 
import time
import os
import sys
import copy
import threading

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
        soup = BeautifulSoup(nover.text,"lxml")
        patten = re.compile('<dd> <a style="" href="(.*?)">')
        #提取链接正则
        urls = re.findall(patten,nover.text)
        bookname = soup.h1.text
        string = ''.join([bookname,'.txt'])
        for i in urls:
            one_bookurl.append('https://www.xuanhuanwu.com' + i)
        one_bookurl.append(string)
    return one_bookurl


def book_down(one_bookurl):
    #lock = threading.Lock()
    def get(url):
        #lock.acquire()
        try:
            time.sleep(5)
            r = requests.get(url, allow_redirects=False, timeout=10)
            soup = BeautifulSoup(r.text,'lxml')
            dd = str(soup.find_all(id = 'content'))
            title = str(soup.h1.string)
            dd = ''.join(['\n\n',title,'\n\n',dd[61:-47]])
            strs = re.sub('<br/><br/>', '\n', dd)
            c=str(one_bookurl.index(url))
            strs='\n\n' + 'QWESDFA' + c + 'RTYHH' + strs + 'SAFASDF' + '\n\n'
            #细剪正文
            with open(one_bookurl[-1],'a',encoding= 'utf-8')as f:
                f.write(strs)
        finally:
            #lock.release()
            r.ok
            pass
    print(u'多线程抓取')
    ts = [threading.Thread(target=get, args=(url,)) for url in one_bookurl[:-2]]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    print(''.join([one_bookurl[-1][:-4],' 下载完成','文件在:',os.getcwd()]))


def combination():
    import wkp #我自己写的模块
    with open('C:\\ProgramData\\Anaconda3\\my_py\\六迹之梦魇宫.txt','rb')as f:
        d = f.read().decode('utf-8')   
    patther = re.compile('QWESDFA(.*?)RTYHH(.*?)SAFASDF',re.S)
    strz = re.findall(patther,d)
    list_number=[]
    for i in range(len(strz)):
        list_number.append(int(strz[i][0]))
    list_new=copy.deepcopy(list_number)
    list_number=wkp.mp(list_number) #冒泡排序
    for i in range(len(strz)):
        numberz=(list_new.index(list_number[i]))
        with open('C:\\ProgramData\\Anaconda3\\六迹之梦魇宫.txt','a')as f:
            f.write(strz[numberz][1])

            
def down(ranges):
    t1 = time.time()
    book_down(one_book_url(books_url(ranges)))
    combination()
    print('\n用时: ' +  str((time.time() - t1))[:-13] + '秒')
    #ranges = int(input('输入玄幻屋的书号:'))

__name__=='__main__'    

down(71)
