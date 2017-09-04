# _*_ coding:utf-8 _*_

import urllib
import urllib.request
import urllib.error
import re


# page = 1
# url = 'https://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
# headers = {'User-Agent': user_agent}

# try:
#     request = urllib.request.Request(url, headers=headers)
#     response = urllib.request.urlopen(request)
#     # print(response.read())
#     content = response.read().decode('utf-8')
#     # print(content)
#     # pattern = re.compile('<div.*?author">.*?<img.*?>(.*?)</a>.*?<div.*?' +
#     #  'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
#     pattern = re.compile(
#         r'<div.*?author clearfix">.*?<a.*?<h2.*?>(.*?)</h2>.*?<div.*?content">.*?<span.*?>(.*?)</span>(.*?)'
#         '<div class="stats.*?class="number">(.*?)</i>',
#         re.S)
#     items = re.findall(pattern, content)
#     for item in items:
#         print("item = ", item)
#         print(item[0], item[1], item[2])
# except urllib.error.URLError as e:
#     if hasattr(e, "code"):
#         print(e.code)
#     if hasattr(e, "reason"):
#         print(e.reason)


class Qsbk(object):
    """糗事百科爬虫类"""

    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enbale = False

    def get_page(self, page_index):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(page_index)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            return None

    def get_page_items(self, page_index):
        page = self.get_page(page_index)
        if not page:
            print("page load error!")
            # return None
        pattern = re.compile(
            r'<div.*?author clearfix">.*?<a.*?<h2.*?>(.*?)</h2>.*?<div.*?content">.*?<span.*?>(.*?)</span>(.*?)'
            '<div class="stats.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, page)
        # page_stories = []
        for item in items:
            print("用户名:{}".format(item[0]))
            print("段子内容:{}".format(item[1]))
            print("点赞人数:{}".format(item[2]))
            print("评论人数:{}".format(item[3]))
            # page_stories.append(
                # [item[0].strip(), item[1].strip(), item[2].strip()])
        # return page_stories

    def load_page(self):
        if self.enbale is True:
            if len(self.stories) < 2:
                pagestories = self.get_page_items(self.page_index)
                if pagestories:
                    self.stories.append(pagestories)
                    self.page_index += 1

    def get_one_story(self, pagestories, page):
        for story in pagestories:
            inpu = input()
            self.load_page()
            if inpu == "Q":
                self.enbale = False
                return
            print("第%d页\t发布人：%s\t 赞：%s\n%s" %
                  (page, story[0], story[2], story[1]))

    def start(self):
        self.get_page_items(self.page_index)
        # print("正在读取，回车查看，Q退出")
        # self.enable = True
        # self.load_page()
        # nowpage = 0
        # while self.enable:
        #     if len(self.stories) > 0:
        #         pagestories = self.stories[0]
        #         nowpage += 1
        #         del self.stories[0]
        #         self.get_one_story(pagestories, nowpage)

qsbk = Qsbk()
qsbk.start()
