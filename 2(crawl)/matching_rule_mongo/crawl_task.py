#匹配规则主要逻辑
"""
 * 你可能会认为你读得懂以下的代码。但是你不会懂的，相信我吧。
 * 要是你尝试玩弄这段代码的话，你将会在无尽的通宵中不断地咒骂自己为什么会认为自己聪明到可以优化这段代码。
 * 现在请关闭这个文件去玩点别的吧。
"""

from bs4 import BeautifulSoup
import requests,re,json,copy,os,time
from gevent import monkey,pool; monkey.patch_socket()
import gevent
from tld import get_tld
import DB_Connect
import DB_Operation
from  newspaper import  Article
from urllib.parse import urljoin
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from fake_useragent import UserAgent
import queue
ua = UserAgent()

class crawl_obj:
    def __init__(self,concurrency=20):#并发个数
        self.mongo_obj = DB_Operation.collection_db()#mongo数据库对象
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': ua.random
        }
        self.proxies ={}#requestsd的代理
        self.timeout = 30
        self.phant_path = '/home/topinfo/phantomjs-2(crawl).1.1-linux-x86_64/bin/phantomjs'#无头浏览器的路径
        self.pgevent = pool.Pool(concurrency)


    def parsing_text(self,test):
        html = ''
        try:
            encode = test.encoding.upper()
        except:
            return html
        if encode == 'UTF-8':
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

    def save_data(self,html,url):
        try:
            tmp_dict = {}
            start = time.time()
            for count, item in enumerate(self.Task_Match_rule):
                tmp = [item[i:i + 2] for i in range(0, len(item), 2)]
                #print('匹配规则：', tmp)
                #print('匹配字段', self.Task_Match_field[count])
                #print('url:', url)
                match_res = self.match_result(html, tmp)
                if 'ontent' in self.Task_Match_field[count]:
                    pass
                else:
                    if 'path' in self.Task_Match_field[count]:
                        dr = re.compile(r'<[^>]+>', re.S)
                        match_res = dr.sub('', str(match_res))
                    else:
                        match_res = str(match_res).replace('</a>',',</a>')
                        dr = re.compile(r'<[^>]+>', re.S)
                        match_res = dr.sub('', str(match_res))
                        match_res = self.validatechar(str(match_res))
                #print('匹配结果为：', match_res,type(match_res))
                tmp_dict[self.Task_Match_field[count]] =  match_res
                # 将数据写入数据库
            try:
                """
                self.db_obj.insert_Crawl_Task_Rule(self.Task[-1],self.domain,url,tmp_dict['title'],tmp_dict['description'],tmp_dict['keywords'],
                                                   tmp_dict['path'],tmp_dict['content'],self.auto_content(html)
                                                   )
            """

                auto_content = self.auto_content(html)
                if auto_content and len(auto_content)>100:
                    tmp = {'Task_RID': self.Task[-1], 'Rule_Domain': self.domain, 'Rule_URL': url,
                           'Rule_Match_T': tmp_dict['title'], 'Rule_Match_D': tmp_dict['description'],
                           'Rule_Match_K': tmp_dict['keywords'],
                           'Rule_Match_P': tmp_dict['path'], 'Rule_Match_C': tmp_dict['content'],
                           'Rule_Match_Cs': auto_content
                           }
                    self.mongo_obj.insert_data(tmp)

            except Exception as e:
                print('写入数据库错误', e)
            #print('save用时：', time.time() - start)
        except Exception as e:
            print ('出错：',e)


    def clear_url_getdata(self, task_id):  # 清理该任务ID的全部结果
        pass

    def auto_content(self, html):  # 自动匹配正文
        try:
            text = Article(url='', language='zh')
            text.download(input_html=html)
            text.parse()
            return text.text
        except:
            return '0'

    def get(self, url):
        try:
            r = requests.get(url, allow_redirects=False, timeout=self.timeout, headers=self.headersParameters,proxies=self.proxies)
        except:
            print(url)
        else:
            if r.status_code == 200:
                all_link = []
                html = self.parsing_text(r)
                pagesoup = BeautifulSoup(html, 'lxml')
                if not html:
                    return all_link
                # self.db_obj.test1(r.url,html.replace("'",'"'))
                self.save_data(html, r.url)  # 解析保存该页面的内容
                for inner in pagesoup.find_all(name='a', attrs={"href": re.compile('')}):
                    try:
                        url_i = inner.get('href')
                        if 'javascript' in url_i or '#' in url_i:
                            continue
                        url_i = urljoin(url, url_i)
                        if self.filter_url(url_i):
                            all_link.append(url_i)
                    except Exception as e:
                        print(e)
                        pass
                return all_link



    def selenium_get(self,url,q):
        try:
            print ('start crawl')
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities["phantomjs.page.settings.userAgent"] = (ua.random)
            desired_capabilities["phantomjs.page.settings.loadImages"] = False
            #proxy = webdriver.Proxy()
            #proxy.proxy_type = ProxyType.MANUAL
            #proxy.http_proxy = '1.9.171.51:800'
            #proxy.add_to_capabilities(desired_capabilities)
            driver = webdriver.PhantomJS(executable_path=self.phant_path,desired_capabilities=desired_capabilities)
            driver.set_page_load_timeout(30)
            driver.get(url)
            html = driver.page_source
            current_url = driver.current_url
            driver.quit()
        except:
            print(url)
        else:
            #print ('get html:',html)
            print ('get')
            all_link = []
            pagesoup = BeautifulSoup(html, 'lxml')
            if not html:
                q.put([])
                return
            self.save_data(html,current_url)  # 解析保存该页面的内容
            for inner in pagesoup.find_all(name='a', attrs={"href": re.compile('')}):
                try:
                    url_i = inner.get('href')
                    if 'javascript' in url_i or '#' in url_i:
                        continue
                    url_i = urljoin(url,url_i)
                    if self.filter_url(url_i):
                        all_link.append(url_i)
                except Exception as e:
                    print (e)
                    pass
            q.put(all_link)

    def crawl_url(self,tmp_link):
        g = [self.pgevent.spawn(self.get, url) for url in tmp_link]
        gevent.joinall(g)
        return g

    def selenium_crawl_url(self,tmp_link):
        thread_all = []
        result = []
        q = queue.Queue()
        while True:
            tmp = tmp_link[0:20]
            tmp_link=tmp_link[20:]
            if not tmp:
                break
            for url in tmp:
                t = threading.Thread(target=self.selenium_get,args=(url,q))
                t.start()
                thread_all.append(t)
            for thr in thread_all:
                thr.join()
        while not q.empty():
            result.append(q.get())
        print ('获取个数：',len(result))
        return result

    def get_filter_rule(self,data):  # 得到url过滤条件
        self.domain_list = []  # 存放域名规则的列表
        self.dirct_list = []  # 存放目录规则的列表
        self.file_name = []  # 存放文件名称的规则
        self.domain1_list = []  #存放域名规则的列表
        self.dirct1_list = []  # 存放目录规则的列表
        self.file1_name = []  # 存放文件名称的规则
        self.input_url = data[0]
        # 将入口url的根域名解析出来
        url = data[0].replace('//', "(|-|)")
        res_list = url.split('/')  # 将url拆分成域名与目录,文件
        domain = res_list[0].replace("(|-|)", "//")#域名
        try:
            self.domain = get_tld(domain)#获取根域名
        except Exception as e:
            print("unkonw")
        self.domain_list.append(self.domain)#必须包含根域名
        self.Task = data
        Task_On_rule = json.loads(data[1].replace('\\"', '"'))
        Task_Out_rule = json.loads(data[2].replace('\\"', '"'))
        self.Task_Deep = int(data[3])
        self.Task_Match_field = json.loads(data[4].replace('\\"', '"'))
        self.Task_Match_rule = json.loads(data[5].replace('\\"', '"'))
        for item in Task_On_rule:
            tmp = item.split(':')
            if tmp[0] == '0':  # 得到url的过滤分类,域名分类
                self.domain_list.append(":".join(tmp[1:]))
            elif tmp[0] == '1':  # 目录分类
                self.dirct_list.append(":".join(tmp[1:]))
            elif tmp[0] == '2':  # 文件名分类
                self.file_name.append(":".join(tmp[1:]))
        for item in Task_Out_rule:
            tmp = item.split(':')
            if tmp[0] == '0':  # 得到url的过滤分类,域名分类
                self.domain1_list.append(":".join(tmp[1:]))
            elif tmp[0] == '1':  # 目录分类
                self.dirct1_list.append(":".join(tmp[1:]))
            elif tmp[0] == '2':  # 文件名分类
                self.file1_name.append(":".join(tmp[1:]))

    def filter_tags(self, htmlstr):
        # 先过滤CDATA"(?is)<script[^>]*?>.*?<\\/script>"
        re_script = re.compile('(?i)<script[\s\S]*?\<\/script\>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_iframe = re.compile('<\s*iframe[^>]*>[^<]*<\s*/\s*iframe\s*>', re.I)  # style
        re_comment = re.compile('<!--[^>]*-->')#HTML注释
        re_br = re.compile('<br\s*?/?>')#处理换行
        blank_line = re.compile('\n+')
        htmlstr = re_comment.sub('', htmlstr)#去掉HTML注释
        #htmlstr = re_br.sub('', htmlstr)
        htmlstr = blank_line.sub('',htmlstr)
        htmlstr = re_script.sub('', htmlstr)#去掉SCRIPT
        htmlstr = re_style.sub('', htmlstr)#去掉style
        htmlstr = re_iframe.sub('',htmlstr)#去掉iframe
        htmlstr = htmlstr.replace("'", '"')
        # 去掉多余的空行
        return htmlstr

    def validatechar(self, str):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_str = re.sub(rstr, "", str)  # 替换为下划线
        return new_str

    def match_result(self, html_str, step_one=[]):
        html = self.filter_tags(html_str)
        html_list = []
        for count, item in enumerate(step_one):
            if not len(item[0]) or not len(item[1]):  # 其中一个条件不匹配
                # 记录step_one[count]的错误记录
                pass
            tmp_math_list = []
            if '|' in item[0] or '|' in item[1]:  # 代表正则或关系
                split_rule = item[0].split('|')
                for fuck in item[1].split('|'):
                    re_math = ("(.*?)" + fuck + '|').join(split_rule)
                    re_math = re_math + ("(.*?)" + fuck)
                    tmp_math_list.append(re_math)
                re_math = '(?i)' + "|".join(tmp_math_list)
            else:  # 没有或关系
                re_math = '(?i)%s(.*?)%s' % (item[0], item[1])
            tmp = re.findall(re_math, html, re.DOTALL)  # 匹配所有
            if len(tmp):
                for i in tmp:
                    html_list.append(i)  # 将搜索出来的字符串全部添加到列表中
        if html_list:
            for ret in html_list:
                if type(ret) == tuple:
                    for i in ret:
                        if i:
                            return i
                else:
                    return ret  # 用最后一个条件最为分割条件
        return 0

    # 负责过滤url不符合条件的返回0
    def filter_url(self, url):
        url = url.replace('//', "(|-|)")
        res_list = url.split('/')  # 将url拆分成域名与目录，文件
        domain = res_list[0].replace("(|-|)", "//")  # 域名
        flag = True
        domain_flag = True
        drict_flag = True
        file_flag = True
        dirct = "/".join(res_list[1:-1])  # 目录
        file = res_list[-1]  # 文件
        if self.domain_list[0] not in domain:  # 必须包含根域名
            return False
        for item in self.domain_list[1:]:
            domain_flag = False
            if item in domain:
                domain_flag = True
                break
        for item in self.dirct_list:
            drict_flag = False
            if item in dirct:
                drict_flag = True
                break
        for item in self.file_name:
            file_flag = False
            if item in file:
                file_flag = True
                break
        if not (domain_flag and drict_flag and file_flag):
            return False
        for item in self.domain1_list:
            if item in domain:
                flag = False
        for item in self.dirct1_list:
            if item in dirct:
                flag = False
        for item in self.file1_name:
            if item in file:
                flag = False
        return flag

    def get_all_selenium_link(self, input_url="http://www.39.net/"):
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = (ua.random)
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        all_link = []
        driver = webdriver.PhantomJS(executable_path=self.phant_path,desired_capabilities=desired_capabilities)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)  # 这两种设置都进行才有效
        driver.get(input_url)
        html = driver.page_source
        driver.quit()
        pagesoup = BeautifulSoup(html,'lxml')
        for link in pagesoup.find_all(name='a', attrs={"href": re.compile('')}):
            url_i = link.get('href')
            if 'javascript' in url_i or '#' in url_i:
                continue
            url_i = urljoin(input_url, url_i)
            if self.filter_url(url_i):
                all_link.append(url_i)
        return all_link

    def get_all_link(self, input_url="http://www.39.net/"):
        all_link = []
        html = requests.get(input_url, headers=self.headersParameters, timeout=self.timeout)
        html.encoding = html.apparent_encoding
        pagesoup = BeautifulSoup(html.text, 'lxml')
        for link in pagesoup.find_all(name='a', attrs={"href": re.compile('')}):
            url_i = link.get('href')
            if 'javascript' in url_i or '#' in url_i:
                continue
            url_i = urljoin(input_url,url_i)
            if self.filter_url(url_i):
                all_link.append(url_i)
        return all_link

    def run(self,task):
        self.get_filter_rule(task)#得到过滤规则
        all_link = self.get_all_link(self.input_url)
        start = time.time()
        all_link = list(set(all_link))
        inner_all_link = copy.copy(all_link)
        if self.Task_Deep == 0:
            self.Task_Deep = 100
        for _ in range(self.Task_Deep):  # 循环深度大于1
            print('层数：', _, '总计抓取个数', len(inner_all_link))
            Iter_obj = self.crawl_url(inner_all_link)
            inner_all_link=[]
            for link_list in Iter_obj:
                tmp = link_list.get()
                if tmp:
                    inner_all_link.extend(tmp)
            inner_all_link = list(set(inner_all_link))
            for link in inner_all_link:
                if link in all_link:
                    inner_all_link.remove(link)
            all_link.extend(inner_all_link)
            #print ('获取URL个数总计：',len(all_link))
            #print('总计用时：',time.time()-start)

    def selenium_run(self,task):
        self.get_filter_rule(task)#得到过滤规则
        all_link = self.get_all_selenium_link(self.input_url)
        all_link = list(set(all_link))
        start = time.time()
        inner_all_link = copy.copy(all_link)
        if self.Task_Deep == 0:
            self.Task_Deep = 100
        for _ in range(self.Task_Deep):#循环深度大于1
            print('层数：', _, '总计抓取个数', len(inner_all_link))
            #print (inner_all_link)
            Iter_obj = self.selenium_crawl_url(inner_all_link)
            inner_all_link = []
            for link_list in Iter_obj:
                tmp = link_list
                if tmp:
                    inner_all_link.extend(tmp)
            inner_all_link = list(set(inner_all_link))
            for link in inner_all_link:
                if link in all_link:
                    inner_all_link.remove(link)
            all_link.extend(inner_all_link)
            print('获取URL个数总计：', len(all_link))
            print('总计用时：',time.time() - start)


if __name__ =='__main__':

    obj = crawl_obj()

    task = obj.db_obj.test1()[0]
    print (task)
    obj.run(task)

