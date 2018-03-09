from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from fake_useragent import UserAgent
ua = UserAgent()

"""
头条从后台获取数据需要到底部之后然后ajax会再次请求数据，所以需要先将滚动条滚动到底部，但是滚动到底部之后是
不会发送请求还需要上拉滚动条

"""
class crawl_toutiao():
    def __init__(self):
        self.phant_path = "C:/untitled/crawl_wechat_toutiao/crawl_toutiao/phantomjs-2.1.1-windows/bin/phantomjs.exe"
        self.single_scroll_high = 10000#单次滚动条滚动的高度
        self.single_upscroll_high = 50#单词上拉滚动条的高度
        self.max_scoll_num = 2000 #最大滚动次数
    def scrollBot(self,driver,high):  # 模拟滚动,将滚动条滚到底部
        # 将页面滚动条拖到
        try:
            js = "var q=document.documentElement.scrollTop=%s"%high
            driver.execute_script(js)

        except Exception as e:
            print ("滚动出错：",e)
        return driver

    def scrollrdm(self,driver,rdm_high):  # 随机滚动到某一位置
        try:
            js = "var q=document.documentElement.scrollTop=%s" % (rdm_high)
            driver.execute_script(js)
            time.sleep(random.uniform(1,2))
        except:
            pass
        return driver
    def get_high(self,driver):
        js = "var q=document.body.scrollHeight ;return(q)"
        Visual_area_height = driver.execute_script(js)
        return Visual_area_height
    def selenium_get(self, url):
        try:
            print('start crawl')
            # proxy = webdriver.Proxy()
            # proxy.proxy_type = ProxyType.MANUAL
            # proxy.http_proxy = '1.9.171.51:800'
            # proxy.add_to_capabilities(desired_capabilities)
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities["phantomjs.page.settings.userAgent"] = (ua.random)
            desired_capabilities["phantomjs.page.settings.loadImages"] = False
            #options = webdriver.ChromeOptions()
            #options.add_argument('user-agent=%s' % (ua.random))
            path = "/home/topinfo/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
            driver = webdriver.PhantomJS(executable_path=path,desired_capabilities=desired_capabilities)
            driver.maximize_window() # 最大化浏览器
            driver.implicitly_wait(5)
            print (url)
            driver.get(url)
            driver.get(url)
            time.sleep(3)
            cur_high = 0
            record_num = 0
            while True:
                # 设置下拉次数模拟下拉滚动条加载网页
                if cur_high == self.get_high(driver):
                    for i in range(2):
                        tmp = cur_high - cur_high * 0.02
                        driver = self.scrollBot(driver, tmp)
                        time.sleep(random.uniform(1, 3))
                    record_num +=1
                    if record_num >5:
                        break
                    print ("重试次数：",record_num)
                else:
                    record_num = 0
                cur_high = self.get_high(driver)
                driver = self.scrollBot(driver,cur_high)
                tmp = cur_high
                print ("总高度为：",cur_high)
                for i in range(2):
                    tmp = tmp - cur_high * 0.02
                    driver = self.scrollBot(driver, tmp)
                    time.sleep(random.uniform(1, 2))
                for i in range(5):
                    driver = self.scrollBot(driver, cur_high+i*20)
                    time.sleep(random.uniform(1, 3))
                break
            html = driver.page_source
            current_url = driver.current_url
            print (current_url)

        except Exception as e:
            print ("出错：",e)
        else:

            all_link = []
            pagesoup = BeautifulSoup(html, 'html.parser')
            for inner in pagesoup.find_all('div',class_="title-box"):
                print (inner.get("ga_event"))
                print (inner.find("a"))

if __name__ == "__main__":
    obj = crawl_toutiao()
    url = "https://www.toutiao.com/c/user/3525840026/#mid=35"
    obj.selenium_get(url)