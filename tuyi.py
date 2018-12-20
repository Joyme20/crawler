#!/usr/bin/env python
# coding=utf-8

import os
import re
import time
import threading
import urllib
from multiprocessing import Pool, cpu_count

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

DIR_PATH = r"C:\迅雷下载\tuyi"      # 下载图片保存路径


def save_pic(pic_src, pic_cnt):
    """
    将图片下载到本地文件夹
    """
    try:
        img = requests.get(pic_src, headers=HEADERS, timeout=10)
        img_name = "pic_cnt_{}.jpg".format(pic_cnt + 1)
        with open(img_name, 'ab') as f:
            f.write(img.content)
            print(img_name)
    except Exception as e:
        print(e)


def make_dir(folder_name):
    """
    新建套图文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False


def delete_empty_dir(save_dir):
    """
    如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的
    情况但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹
    """
    if os.path.exists(save_dir):
        if os.path.isdir(save_dir):
            for d in os.listdir(save_dir):
                path = os.path.join(save_dir, d)     # 组装下一级地址
                if os.path.isdir(path):
                    delete_empty_dir(path)      # 递归删除空文件夹
        if not os.listdir(save_dir):
            os.rmdir(save_dir)
            print("remove the empty dir: {}".format(save_dir))
    else:
        print("Please start your performance!")     # 请开始你的表演


lock = threading.Lock()     # 全局资源锁


def urls_crawler(url):
    """
    爬虫入口，主要爬取操作
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10).text
        # 套图名，也作为文件夹名
        folder_name = BeautifulSoup(r, 'lxml').find(
            'title').text.encode('ISO-8859-1').decode('utf-8')
        with lock:
            if make_dir(folder_name):
                # 套图张数
                max_count = BeautifulSoup(r, 'lxml').find(
                    'div', class_='page').find_all('a')[-2].get_text()
                # 套图页面
                # page_urls = [url + "/" + str(i) for i in
                #              range(1, int(max_count) + 1)]

                html2 = getHtml(url[0])

                reg = r'data-original="(.+?\.jpg)" '  # 正则表达式，得到图片地址
                imgre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.
                print(type(imgre), type(html))
                html2 = html2.decode("gbk")
                imgUrlList = re.findall(imgre, html2)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据

                # 图片地址
                img_urls = imgUrlList
                print(img_urls)
                # for index, page_url in enumerate(page_urls):
                #     result = requests.get(
                #         page_url, headers=HEADERS, timeout=10).text
                #     # 最后一张图片没有a标签直接就是img所以分开解析
                #     if index + 1 < len(page_urls):
                #         img_url = BeautifulSoup(result, 'lxml').find(
                #             'div', class_='content').find('a').img['src']
                #         img_urls.append(img_url)
                #     else:
                #         img_url = BeautifulSoup(result, 'lxml').find(
                #             'div', class_='content').find('img')['src']
                #         img_urls.append(img_url)

                for cnt, url in enumerate(img_urls):
                    save_pic(url, cnt)
    except Exception as e:
        print(e)

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

def getMainHtml(html):
    reg = r'<a href="(http://www.tuyimm.vip/thread-(.+?)\.html)" '  # 正则表达式，得到每集地址
    htmlre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.

    print(type(htmlre),type(html))
    # if type(html) == "byte":
    html = html.decode("gbk")  #ok

    print(type(htmlre), type(html))
    htmllist = htmlre.findall(html)
    print("htmllist",htmllist)
    return htmllist


if __name__ == "__main__":
    htmllist = []
    try:
        # socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒
        # http://www.tuyimm.com/forum-31-1.html
        # html = "http://www.tuyimm.com/forum-54-"+str(i)+".html" #秀人网
        html = "http://www.tuyimm.vip/forum-332-1.html"  # 魅妍社

        html = getHtml(html)  # import url
        # print("第" + str(i) + "页")
        # print (html)
        htmllist = getMainHtml(html)

    except Exception as e:
        print(Exception, ":", e)
    length = html
    urls = htmllist


    pool = Pool(processes=cpu_count())
    try:
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler, urls)
    except Exception:
        time.sleep(30)
        delete_empty_dir(DIR_PATH)
        pool.map(urls_crawler, urls)