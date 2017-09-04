# /usr/bin/python3
# _*_ coding:utf-8 _*_

import urllib
import urllib.request
import urllib.error
import re


__author__ = 'Arvin.He'


class Qsbk(object):
    """糗事百科爬虫类"""

    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 是否继续运行的变量
        self.enabled = False

    def get_page(self, page_index):
        """根据页面索引,获取页面的HTML文件内容"""
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
                print("连接糗事百科失败，原因：", e.reason)
            return None

    def get_page_items(self, page_index):
        """ 解析HTML文件"""
        page = self.get_page(page_index)
        if not page:
            print("页面加载失败...")
            return None
        # 用正则表达式匹配出作者，段子内容，段子里面的图片，点赞数
        pattern = re.compile(
            r'<div.*?author clearfix">.*?<a.*?<h2.*?>(.*?)</h2>.*?<div.*?content">.*?<span.*?>(.*?)</span>(.*?)'
            '<div class="stats.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, page)
        pagestories = []
        # 遍历items，找出不含img的段子
        for item in items:
            # 是否含有图片,item[2]是图片
            has_img = re.search("img", item[2])
            if not has_img:
                # 除去字符br
                replaceBR = re.compile("<br/>")
                text = re.sub(replaceBR, "\n", item[1])
                # item[0]是一个段子的发布者，item[1]是内容,item[3]是点赞数
                pagestories.append(
                    [item[0].strip(), text.strip(), item[3].strip()])
        return pagestories

    def load_page(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enabled is True:
            if len(self.stories) < 2:
                # 获取新一页
                pagestories = self.get_page_items(self.page_index)
                if pagestories:
                    self.stories.append(pagestories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.page_index += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def get_one_story(self, pagestories, page):
        # 遍历一页的段子
        for story in pagestories:
            i = input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.load_page()
            if i == "Q":
                self.enabled = False
                return
            print("第{}页\t发布人:{}\t 赞：{}\n{}".format(
                page, story[0], story[2], story[1]))

    def start(self):
        print("正在读取糗事百科，按回车键查看新段子，Q退出")
        self.enabled = True
        # 先加载一页内容
        self.load_page()
        # 局部变量，控制当前读到了第几页
        nowpage = 0
        while self.enabled:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pagestories = self.stories[0]
                # 当前读到的页数加一
                nowpage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.get_one_story(pagestories, nowpage)


if __name__ == "__main__":
    qsbk = Qsbk()
    qsbk.start()
