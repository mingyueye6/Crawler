'''
爬取百度图片，将图片保存到本地
代理IP是在全网代理网站上搜的，可能不能用了
'''
import os
import re
import urllib.request
import urllib.parse


class BaiduSpider:
    def __init__(self):
        # 抓取百度图片动态加载的json对象，获取url
        self.baseurl = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={name}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={name}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&selected_tags=&pn={page}&rn=30'
        proxy = {'http': '219.141.153.44:80'}
        # 创建Handler处理器对象
        pro_hand = urllib.request.ProxyHandler(proxy)
        # 创建自定义opener对象
        self.opener = urllib.request.build_opener(pro_hand)
        # 添加User Agent
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def loadpage(self, url, i):
        print('开始解析网页：',url)
        req = urllib.request.Request(url)
        # opener对象open方法
        res = self.opener.open(req)
        try:
            # 有的页面utf-8转换失败，跳过此页
            html = res.read().decode('utf-8')
        except:
            print('-' * 30)
            print('第%d页解析失败' % (i + 1))
            print('-' * 30)
            return
        req = '"thumbURL":"(.*?)",'
        href_list = re.findall(req, html)
        self.saveimg(href_list)

    def saveimg(self, href_list):
        print('页面解析完成，开始下载图片')
        for href in href_list:
            try:
                urllib.request.urlretrieve(href, self.path + href[-25:])
            except:
                # 有的图片下载失败，忽略
                print('下载失败的链接：',href)
        print('下载完成',"\n", '=' * 30)


    def work(self):
        name = input('请输入要爬去图片名称：')
        number = int(input('请输入要爬去的页数(30/页)：'))
        # 判断文件夹是否存在，不存在则创建
        if not os.path.isdir(name):
            os.makedirs(name)
        self.path = name + '/'
        name = urllib.parse.quote(name)
        for i in range(number):
            # 动态爬区所有页面
            url = self.baseurl.format(name=name, page=str(i * 30))
            self.loadpage(url, i)

if __name__ == '__main__':
    spider = BaiduSpider()
    spider.work()