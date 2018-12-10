'''使用selenium + ChromeDriver爬取京东商品信息'''
from selenium import webdriver
import time
import csv


class JdScripy:
    def __init__(self):
        # 把Chrome设置无界面浏览器
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        # 设置代理IP
        opt.add_argument('--proxy-server=http://58.53.128.83:3128')
        # 创建浏览器对象
        self.driver = webdriver.Chrome(options=opt)

    def work(self):
        self.driver.get('https://www.jd.com/')
        # 发送文字到搜索框，点击搜索
        data = input('输入要爬去的商品: ')
        self.driver.find_element_by_class_name('text').send_keys(data)
        self.driver.find_element_by_class_name('button').click()
        with open('%s.csv' % data, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            n = 0
            while True:
                n += 1
                # 动态加载-->全部加载，执行脚本，进度条拉到底部
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
                r_list = self.driver.find_elements_by_xpath('//div[@id="J_goodsList"]//li')
                for r in r_list:
                    m = r.text.split('\n')
                    if m[1][0] == '￥':
                        price = m[0]
                        name = m[3]
                        commit = m[4]
                        market = m[5]
                    else:
                        price = m[0]
                        name = m[1]
                        commit = m[2]
                        market = m[3]
                    # print([name, price, commit, market])
                    L = [name.strip(), price.strip(), commit.strip(), market.strip()]
                    writer.writerow(L)
                print('第%d页爬去结束' % n)
                # 点击一页
                if self.driver.page_source.find('pn-next disabled') != -1:
                    self.driver.find_element_by_class_name('pn-next').click()
                else:
                    print('抓取结束,共抓取了%d页' % n)
        self.driver.quit()


if __name__ == "__main__":
    spider = JdScripy()
    spider.work()