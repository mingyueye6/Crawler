'''爬取链家二手房数据，保存到数据库'''
import requests
import re
import pymysql
import warnings


class LianjiaSpider:
    def __init__(self):
        self.baseurl = "https://sz.lianjia.com/ershoufang/"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.proxies = {"http": "http://119.190.188.29:8060"}
        self.db = pymysql.connect("localhost", "root", "00000000", charset="utf8")
        self.cursor = self.db.cursor()

    def getPage(self, url):
        print("正在解析网页：", url)
        res = requests.get(url, proxies=self.proxies, headers=self.headers, timeout=5)
        res.encoding = "utf-8"
        html = res.text
        p = '<span class="houseIcon".*?data-el="region">(.*?)</a>.*?target="_blank">(.*?)</a>.*?class="totalPrice"><span>(.*?)</span>(万)</div>'
        r_list = re.findall(p, html, re.S)
        # [('潜龙鑫茂花园B区 ', '民治', '376', '万'),...]
        self.writeTomysql(r_list)

    def writeTomysql(self, r_list):
        print("页面解析完成,正在存入数据库...")
        ins = "insert into lianjia(housename, address, totalprice) values(%s, %s, %s)"
        for r_tuple in r_list:
            name = r_tuple[0].strip()
            add = r_tuple[1].strip()
            price = r_tuple[2].strip() + r_tuple[3].strip()
            L = [name, add, price]
            self.cursor.execute(ins, L)
            self.db.commit()
        print("存入数据库成功")

    def workOn(self):
        # 创建要保存数据的 库/表
        c_db = "create database if not exists Lianjiadb character set utf8"
        u_db = "use Lianjiadb"
        c_tab = """create table if not exists lianjia( 
                                 id int primary key auto_increment,
                                 housename varchar(20), 
                                 address varchar(10),
                                 totalprice varchar(10))charset=utf8"""
        # 如果 数据库/表 已经存在，创建时会抛出警告，使用warnings忽略警告错误的输出
        warnings.filterwarnings("ignore")
        try:
            self.cursor.execute(c_db)
            self.cursor.execute(u_db)
            self.cursor.execute(c_tab)
        except Warning:
            pass
        # 获取总页数
        print('正在解析网页：',self.baseurl)
        res = requests.get(self.baseurl, proxies=self.proxies, headers=self.headers, timeout=5)
        res.encoding = "utf-8"
        html = res.text
        req = '''<div class="page-box house-lst-page-box" comp-module='page' page-url="/ershoufang/pg{page}/"page-data='{"totalPage":(.*?),"curPage":1}'>'''
        pages = re.findall(req, html)[0]
        print('获取总页数成功：',pages)
        for page in range(1, int(pages) + 1):
            # 拼接url,访问每页的数据
            url = self.baseurl + 'pg' + str(page)
            self.getPage(url)
        # 断开数据库连接
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    spider = LianjiaSpider()
    spider.workOn()
