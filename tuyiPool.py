# -*- coding: utf-8 -*-
import socket
import urllib

import time
import urllib.request
import re
# content = urllib.reguest.urlopen('http://www.tuyimm.com/thread-8165-1-1.html').read()
import os
from multiprocessing import Pool, cpu_count


def getHtml(url):
    try:
        page = urllib.request.urlopen(url)  # urllib.urlopen()方法用于打开一个URL地址
        print(page)
        html = page.read()  # read()方法用于读取URL上的数据
        return html
    except Exception as e:
        print(Exception, ":", e)


def getImg(html, pageNum):
    reg = r'data-original="(.+?\.jpg)" '  # 正则表达式，得到图片地址
    imgRe = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.
    html = html.decode("gbk")
    imgList = re.findall(imgRe, html)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据

    reg2 = r'<title>(.+?)</title>'
    titleRe = re.compile(reg2)
    title = re.findall(titleRe, html)[0]

    # pageNum = urls[-6, -5]
    path1 = 'C:\\迅雷下载\\tuyiyouguoquan\\' + pageNum + "\\"
    # path1 = 'C:\\迅雷下载\\tuyi3\\'

    # if os.path.exists(path1):
    #     print(pageNum, "文件夹已存在")
    # else:
    #     os.mkdir(path1)
    title = title[22:-18]
    path2 = path1 + title
    if os.path.exists(path2):
        print(pageNum, title, "文件夹已存在")
    else:
        os.mkdir(path2)

    imgCnt = 1
    for imgUrl in imgList:
        if os.path.exists(path2 + '\%s.jpg' % imgCnt):
            print(pageNum, title, imgCnt, "文件已存在")
        else:
            urllib.request.urlretrieve(imgUrl, path2 + '\%s.jpg' % imgCnt)
            print(pageNum, title, imgCnt, "文件已下载")
        imgCnt = imgCnt + 1
    return imgList


def getMainHtml(html):
    reg = r'<a href="(http://www.tuyimm.vip/thread-(.+?)\.html)" '  # 正则表达式，得到每集地址
    htmlRe = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.

    print(type(htmlRe), type(html))
    html = html.decode("gbk")  # ok

    print(type(htmlRe), type(html))
    htmlList = re.findall(htmlRe, html)

    print("htmlList", htmlList)
    return htmlList


def main(urls):
    html = getHtml(urls)  # import url
    htmlList = getMainHtml(html)
    cnt = 0
    print(htmlList)
    for html in htmlList:
        html2 = getHtml(html[0])
        # 从每一页的url中截取页数
        pageNum = urls[-6: -5]  # way1
        getImg(html2, pageNum)
        cnt += 1
        # print(name)


if __name__ == "__main__":
    urls = ["http://www.tuyimm.vip/forum-342-{cnt}.html".format(cnt=cnt)
            for cnt in range(1, 6)]
    pool = Pool(processes=cpu_count())

    try:
        pool.map(main, urls)
        # str = '[YOUMI尤蜜荟] 2016.12.27 Vol.002 周琰琳LIN [44+1P-159M]（图意网）'
        # print(str[22:-18])
        # http://www.tuyimm.com/forum-31-1.html
        # html = "http://www.tuyimm.com/forum-54-"+str(i)+".html" #秀人网

        # for i in range(2, 11):
        #     html = "http://www.tuyimm.vip/forum-332-" + str(i) + ".html"  # 魅妍社
    except Exception as e:
        print(Exception, ":", e)
