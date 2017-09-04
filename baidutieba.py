# /usr/bin/python3
# _*_ coding:utf-8 _*_

import urllib
import urllib.request
import urllib.error
import re


__author__ = 'Arvin.He'


class Tool(object):
    """处理页面标签类"""
    # 去除img标签,7位长空格
    rmImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    rmAddr = re.compile('<a.*?>|</a>')
    # 将换行的标签换为\t
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表符<td>替换成\t
    replaceTD = re.compile('<td>')
    # 将段落开头位\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    rmExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.rmImg, "", x)
        x = re.sub(self.rmAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n  ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.rmExtraTag, "", x)
        return x.strip()


class BaiduTieBa(object):
    """百度贴吧爬虫类"""

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, base_url, seeLZ, floorTag):
        # base链接地址
        self.base_url = base_url
        # 是否只看楼主
        self.seeLZ = '?see_lz=' + str(seeLZ)
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = "百度贴吧"
        # 是否写入楼分隔符的标记
        self.floorTag = floorTag

    def get_page(self, page_num):
        # 传入页码，获取该页帖子的代码
        try:
            url = self.base_url + self.seeLZ + '&pn' + str(page_num)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # print(response.read())
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print("连接百度贴吧失败,错误原因:", e.reason)
                return None

    # 获取帖子标题
    def get_title(self, page):
        # 得到标题的正则表达式
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取帖子的总页数
    def get_page_num(self, page):
        # 获取帖子页数的正则表达式
        pattern = re.compile(
            '<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取每一楼层的内容,传入页面内容
    def get_content(self, page):
        # 匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    def set_file_title(self, title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def write_data(self, contents):
        # 向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == "1":
                # 楼层分隔符
                floorLine = "\n" + str(self.floor) + \
                    "----------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item.decode('utf-8'))
            self.floor += 1

    def start(self):
        index_page = self.get_page(1)
        page_num = self.get_page_num(index_page)
        title = self.get_title(index_page)
        self.set_file_title(title)
        if page_num is None:
            print("URL 已失效,请重试")
            return
        try:
            print("该帖子共有{}页".format(page_num))
            for i in range(1, int(page_num) + 1):
                print("正在写入第{}页数据".format(i))
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
        except IOError as e:
            print("写入异常, 原因:{}".format(e.message))
        finally:
            print("写入任务完成")


if __name__ == "__main__":
    print("请输入帖子代号")
    base_url = 'http://tieba.baidu.com/p/' + \
        str(input('http://tieba.baidu.com/p/'))
    seeLZ = input("是否只获取楼主发言，是输入1，否输入0\n")
    floorTag = input("是否写入楼层信息，是输入1，否输入0\n")
    bdtb = BaiduTieBa(base_url, seeLZ, floorTag)
    bdtb.start()


# if __name__ == "__main__":
#     # whole url = https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1
#     base_url = 'http://tieba.baidu.com/p/3138733512'
#     bdtb = BaiduTieBa(base_url, 1)
#     bdtb.get_page(1)
