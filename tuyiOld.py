# -*- coding: utf-8 -*-
import socket
import urllib

import time
import urllib.request
import re
#content = urllib.reguest.urlopen('http://www.tuyimm.com/thread-8165-1-1.html').read()
import os
# from selenium import webdriver
from bs4 import BeautifulSoup
from django.contrib.sites import requests

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

def getHtml(url):
    try:
    #     url.decode("gbk2312")
        page = urllib.request.urlopen(url)  #urllib.urlopen()方法用于打开一个URL地址
        print(page)
        html = page.read()  # read()方法用于读取URL上的数据
        # html = html.decode("gb2312")  # 设置解码方式 不填默认解码成str
        # str(html, encoding="GBK")
        # page.close()  # 注意关闭response
        # print(1,html,type(html))

        return html

    except Exception as e:
        print (Exception, ":", e)


def getImg(html,name,i):
    # html = html.decode("gb2312")  # python3
    print("getimg",html)

    reg = r'data-original="(.+?\.jpg)" '    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    print(type(imgre),type(html))
    html =html.decode("gbk")
    imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    # str(html, encoding="GBK")
    # result = re.match(reg, html)
    # 把筛选的图片地址通过for循环遍历并保存到本地
    # 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名

    # r = requests.get(html, headers=HEADERS, timeout=10).text
    # # 套图名，也作为文件夹名
    # folder_name = BeautifulSoup(r, 'lxml').find(
    #     'title').text.encode('ISO-8859-1').decode('utf-8')

    path1 = 'C:\\迅雷下载\\tuyi\\'+str(i)+"\\"
    if os.path.exists(path1):
        print(i,"文件夹已存在")
    else:
        os.mkdir(path1)
    path2 = path1+str(name)
    if os.path.exists(path2):
        print(i,name,"文件夹已存在")
    else:
        os.mkdir(path2)

    num = 1
    for imgurl in imglist:
        if os.path.exists(path2+'\%s.jpg' %num):
            print(i,name,num,"文件已存在")
        else:
            # try:
                urllib.request.urlretrieve(imgurl, path2 + '\%s.jpg' % num)
                print(i,name,num,"文件已下载")

                # print(i+"/"+name+"/"+x)
                # time.sleep(1)  # 自定义
            # except Exception as e:
            #     print (Exception, ":", e)
        num = num + 1

    # time.sleep()  # 自定义
    return imglist

def getMainHtml(html):
    reg = r'<a href="(http://www.tuyimm.vip/thread-(.+?)\.html)" '  # 正则表达式，得到每集地址
    htmlre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.

    print(type(htmlre),type(html))
    # if type(html) == "byte":
    html = html.decode("gbk")  #ok

    print(type(htmlre), type(html))
    htmllist = re.findall(htmlre, html)

    print("htmllist",htmllist)
    return htmllist


# html = getHtml("http://www.tuyimm.com/thread-8165-1-1.html")
# print (getImg(html,1))


# browser = webdriver.Chrome()

try:
    # socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
    # http://www.tuyimm.com/forum-31-1.html
    # html = "http://www.tuyimm.com/forum-54-"+str(i)+".html" #秀人网
    for i in range(2,11):
        html = "http://www.tuyimm.vip/forum-332-"+str(i)+".html" #魅妍社

        html = getHtml(html)   #import url
        # print("第" + str(i) + "页")
        # print (html)
        htmllist = getMainHtml(html)
        name = 0
        print (htmllist)
        for html in htmllist:
            # path = "C:\\Users\laomingming\Desktop\chromedriver.exe"
            # browser = webdriver.Chrome(executable_path=path)
            # browser.get(html)
            # html2 = browser.page_source
            print("html",html,type(html[0]))
            # html = html.decode("gbk")
            html2 = getHtml(html[0])
            # html2.decode("gb2312")
            # print(type(html2),html2)
            print("html2",html2,type(html2[0]))

            print("html2", html2[0])
            print (getImg(html2,name,i))
            # browser.close()


            # print (html2)
            name += 1
            print(name)
            time.sleep(2)  # 自定义
except Exception as e:
    print (Exception, ":", e)



# print (htmllist)
