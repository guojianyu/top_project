import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
from  newspaper import  Article
from gevent import monkey,pool; monkey.patch_socket()
import gevent
from fake_useragent import UserAgent
ua = UserAgent()

class Baidu_compare():
    def __init__(self,concurrency=100,get_page_count=3):
        self.pgevent = pool.Pool(concurrency)
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': ua.random
        }
        self.proxies = {}# requestsd的代理
        self.timeout = 30
        self.get_page_count = get_page_count

    def filter_tags(self, htmlstr):
        # 先过滤CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_script.sub('', htmlstr)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        return s

    def page_turning(self, root):
        all_search_info = []
        for _ in range(1, self.get_page_count):  # 翻多少页
            try:
                next_page = root.xpath("//div[@id='page']/a[@class='n']/@href")[-1]
                next_page = 'http://www.baidu.com' + next_page
                r = requests.get(next_page, headers=self.headersParameters, timeout=self.timeout)
                html = self.parsing_text(r)
                root = etree.HTML(r.content)
                soup = BeautifulSoup(html, 'lxml')
                # print (len(soup.findAll('div',{'id':'content_left'})))
                for item in soup.findAll('div', {'class': 'result'}):
                    a_url = item.find('a')
                    head = a_url.text
                    url = a_url.get('href')
                    baidu_summary = item.find('div', {'class': 'c-abstract'}).text
                    baidu_summary = self.filter_tags(baidu_summary)
                    tmp = [head, url, baidu_summary]
                    all_search_info.append(tmp)
            except:#翻页出错，直接退出
                break
        return all_search_info

    def parsing_text(self,test):
        html = ''
        encode = test.encoding.upper()
        if  encode== 'UTF-8':
            html = test.text
        elif encode == 'ISO-8859-1':
            try:
                html = test.text.encode('ISO-8859-1').decode('gbk').encode('utf-8').decode('utf-8')
            except:
                try:
                    html = test.text.encode('ISO-8859-1').decode('utf-8')
                except:
                    test.encoding = test.apparent_encoding
                    html = test.text
        else:
            test.encoding = test.apparent_encoding
            html = test.text

        return html

    def input_url(self,keyword):
        try:
            all_search_info = []
            url = 'http://www.baidu.com/s?wd=%s' % '"' + keyword + '"'  # 进入搜索首页
            print (url)
            r = requests.get(url, timeout=self.timeout, headers=self.headersParameters,
                             proxies=self.proxies)
            html = self.parsing_text(r)
            root = etree.HTML(r.content)
            soup = BeautifulSoup(html,'lxml')
            for item in soup.findAll('div',{'class':'result'}):
                a_url = item.find('a')
                head = a_url.text
                url = a_url.get('href')
                baidu_summary = item.find('div', {'class': 'c-abstract'}).text
                baidu_summary = self.filter_tags(baidu_summary)
                tmp = [head,url,baidu_summary]
                all_search_info.append(tmp)
            a =self.page_turning(root)
            all_search_info.extend(a)#获得该关键字多少页的数据
            print (len(all_search_info))

            """
            for i in all_search_info:
                print (i)
            """
            return keyword,all_search_info#将搜索词和百度搜索页的结果返回
        #self.crawl_search_url(keyword,all_search_info)
        except:
            return

    def get_text(self, url):
        text = Article(url='', language='zh', headers=self.headersParameters, timeout=self.timeout)
        test = requests.get(url, headers=self.headersParameters, timeout=self.timeout)
        test.encoding = test.apparent_encoding
        html = test.text
        text.download(input_html=html)
        text.parse()
        # print ('parse 用时:',time.time()-start)
        return test.url, text

    def single_url(self,keyword,all_search_info):
        try:
            url = all_search_info[1]
            head = all_search_info[0]
            baidu_sumarry = all_search_info[2]
            res_url, content_txt = self.get_text(url)  # 请求超时
            meta_description = content_txt.meta_description
            meta_keywords = content_txt.meta_keywords
            meta_title = content_txt.title
            print (keyword, res_url, baidu_sumarry, meta_title, meta_description, meta_keywords)
        except:
            return 'timeout'

    def crawl_input(self,keywords):
        g = [self.pgevent.spawn(self.input_url, keyword) for keyword in keywords]
        gevent.joinall(g)
        return g

    def crawl_search_url(self,keyword,all_search_info):
        g = [self.pgevent.spawn(self.single_url,keyword,single_info) for single_info in all_search_info]
        gevent.joinall(g)

    def run(self,keywords):
        all_info = self.crawl_input(keywords)
        for item in all_info:
            tmp = item.get()
            if tmp:
                self.crawl_search_url(tmp[0],tmp[1])

if __name__ == '__main__':
    import time
    start = time.time()
    a = Baidu_compare()
    #a.input_url()
    a1 = ['肝病','肺病']
    a.run(a1)
    print (time.time()-start)