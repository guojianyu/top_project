import requests
import re,time
from bs4 import BeautifulSoup
from lxml import etree
import DB_Operation
import jieba.analyse
import math
from  newspaper import Article
from gevent import monkey,pool; monkey.patch_socket()
import gevent
from fake_useragent import UserAgent
ua = UserAgent()
get_page_count =1#比对前几页的文章
req_timeout = 30#请求url的超时事件

class Baidu_compare():
    def __init__(self,concurrency=100,get_page_count=1):
        self.pgevent = pool.Pool(concurrency)
        self.db_obj = DB_Operation.collection_db()
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': ua.random
        }
        self.proxies = {} # requestsd的代理
        self.timeout = 30
        self.get_page_count = get_page_count

    def Article_split_sentence(self,content):
        symbol = ["。", "！", "?", "!", "？"]
        sentences = re.split(str(symbol), content)
        return sentences
    def save_keyword_sentence(self,keyword,sentence):
        try:
            self.db_obj.insert_keyword_sentence({"Keyword":keyword,"Sentence":sentence})
        except:
            pass

    def keyword_in_sentences(self,keywords,content):
        sentences = self.Article_split_sentence(content)
        for keyword in keywords:
            for sentence in sentences:
                if keyword in sentence:
                    self.save_keyword_sentence(keyword,sentence)

    def filter_tags(self,htmlstr):
        #先过滤CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#处理换行
        re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_script.sub('',htmlstr) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        return s

    def save_data(self):
        pass
        """
        try:
            self.db_obj.insert_Compare_List(rid, max_simil_url, summary_url, meta_description, content_url,
                                       article_summary, tmp_ci, round(max_simil, 2), meta_title,
                                       ",".join(meta_keywords))
            # 将文章和从搜索引擎搜索出来的最大相似文章记录

            self.db_obj.update_compare_flag(rid)  # 文章数据库标识得到结果
            for related_txt in related_search:  # 将相关搜索词条插入数据库
                self.db_obj.insert_Compare_Related(rid, related_txt)
        except Exception as e:
            print(e)
            print('3:出错id:', rid, '标题：', meta_title, '描述：', meta_description, '关键字：', meta_keywords)
            print('文章摘要：', parse_article_summary)
        """

    def get_url(self,data):
        try:
            rid = data["_id"]  # 文章的id
            title = data["Rule_Match_T"]  # 文章的标题1
            title = re.sub('-', '_', re.sub('\(.*?\)', '', title)).split('_')
            if len(title[0]) < 5:
                title = "".join(title)
            else:
                title = title[0]
            content = data["Rule_Match_Cs"]  # 文章的内容15
            # print('content:', content)
            input_url = 'http://www.baidu.com/s?wd=%s' % '"' + title + '"'  # 进入搜索首页
            r = requests.get(input_url,timeout=self.timeout, headers=self.headersParameters,
                             proxies=self.proxies)
        except:

            return
        else:
            if r.status_code == 200:
                all_search_info = []
                root = etree.HTML(r.content)
                html = self.parsing_text(r)
                soup = BeautifulSoup(html, 'lxml')
                for item in soup.findAll('div', {'class': 'result'}):
                    try:
                        a_url = item.find('a')
                        url = a_url.get('href')
                        baidu_summary = item.find('div', {'class': 'c-abstract'}).text
                        baidu_summary = self.filter_tags(baidu_summary)
                        tmp = [url, baidu_summary]
                        all_search_info.append(tmp)
                    except:
                        #print ("出错")
                        #print (url)
                        #print (input_url)
                        pass

                if len(all_search_info) <= 0:
                    self.db_obj.update_article_search(rid,'2')# 百度搜索框没有结果
                    return
                related_search = root.xpath("//div[@id='rs']/table/tr/th/a/text()")#相关搜索
                res1 =self.cut_word(content)
                parse_article_summary = ''
                try:
                    for item in range(6):
                        tmp1 = re.search('.{0,25}%s.{0,25}' % res1[item][0], content.strip(), re.DOTALL)  # 从文章截取标题
                        if tmp1:
                            parse_article_summary = "...".join([parse_article_summary, tmp1.group(0)])
                except:  # 没有网页内容
                    pass
                self.save_summary_related(parse_article_summary,related_search,str(rid))#保存百度的相关搜索与文章摘要
                u = self.page_turning(root)
                all_search_info.extend(u)
                return all_search_info,data
            return

    def page_turning(self, root):
        all_search_info = []
        for _ in range(1, self.get_page_count):  # 翻多少页
            try:
                next_page = root.xpath("//div[@id='page']/a[@class='n']/@href")[-1]
                next_page = 'http://www.baidu.com' + next_page
                r = requests.get(next_page, headers=self.headersParameters, timeout=self.timeout)
                html = self.parsing_text(r)
                root = etree.HTML(r.content)
                soup = BeautifulSoup(html,'lxml')
                # print (len(soup.findAll('div',{'id':'content_left'})))
                for item in soup.findAll('div', {'class': 'result'}):
                    a_url = item.find('a')
                    head = a_url.text
                    url = a_url.get('href')
                    baidu_summary = item.find('div', {'class': 'c-abstract'}).text
                    baidu_summary = self.filter_tags(baidu_summary)
                    tmp = [url, baidu_summary]
                    all_search_info.append(tmp)
            except:  # 翻页出错，直接退出
                break
        return all_search_info

    def parsing_text(self, test):
        html = ''
        encode = test.encoding.upper()
        if encode== 'UTF-8':
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

    def get_text(self,url):
        headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': ua.random
        }
        text = Article(url='', language='zh', headers=headersParameters, timeout=req_timeout)

        test = requests.get(url, headers=headersParameters, timeout=req_timeout)
        test.encoding = test.apparent_encoding
        html = test.text
        text.download(input_html=html)
        text.parse()
        # print ('parse 用时:',time.time()-start)
        return test.url, text

    def get_url_result(self,url,summary,data):#爬取url
        #print(url)
        #print (summary)
        #print(data)
        #self.keyword_in_sentences()
        try:
            rid = data["_id"]
            Article_Keywords = data["Article_Keywords"]  # 文章的内容15
            symbol = [":", "|"]
            item = re.split(str(symbol), Article_Keywords)
            res1 = [item[i:i + 2] for i in range(0, len(item), 2)]
            res1.pop(-1)
            res_url, content_txt = self.get_text(url)  # 请求超时
            res2 = self.cut_word(content_txt.text)
            vectors = self.tf_idf(res1=res1, res2=res2)
            similarity = self.run(vector1=vectors[0], vector2=vectors[1])
            print ('url:',url)
            print( '相似度:', similarity)
            print ('百度摘要:',summary)
            ciping_url = res2
            url_content = content_txt.text
            meta_description = content_txt.meta_description
            meta_keywords = content_txt.meta_keywords
            meta_title = content_txt.title
            article_summary = ''
            try:
                for item in range(6):
                    tmp = re.search('.{0,25}%s.{0,25}' % ciping_url[item][0], url_content.strip(),
                                    re.DOTALL)  # 从文章截取标题
                    if tmp:
                        article_summary = "...".join([article_summary, tmp.group(0)])
            except:  # 没有网页内容
                pass

            Article_Keyword = ""
            Article_keywords = ""
            tmp = []
            for ci in ciping_url:
                Article_keywords = "".join([Article_Keywords, ci[0], ":", str(round(ci[1], 2)), '|'])
                Article_Keyword = "".join([Article_Keyword, ci[0], '|'])
                tmp.append(ci[0])
            self.keyword_in_sentences(tmp,url_content)
            try:
                self.db_obj.insert_data({"Article_RID":str(rid),"Compare_URL":res_url," Compare_Title":meta_title,
                                         "Compare_Keywords":meta_keywords,"Compare_Description":meta_description,"Compare_Content":url_content,
                                         "Compare_Summary_Baidu":summary,"Compare_Summary":article_summary,"Article_Keyword":Article_Keyword,
                                        "Article_keywords":Article_keywords,"Compare_Article_Similar":similarity,
                                         })
                self.db_obj.update_article_search(rid,"1")# 文章数据库标识得到结果
            except Exception as e:
                print ('插入数据库错误:',e)
        except:
            pass

    def crawl_url(self, data_col): # 并发搜索关键字的返回的所有结果的url
        crawl_url_list = []
        for data in data_col:
            data = data.get()
            if not data:
                print('出错')#出错或者没有搜索结果
                continue
            else:
                for item in data[0]:
                    url = item[0]#百度跳转的url
                    summary = item[1]#百度摘要
                    crawl_url_list.append(self.pgevent.spawn(self.get_url_result,url,summary,data[1]))
        gevent.joinall(crawl_url_list)
        return  crawl_url_list

    def crawl_keys_url(self,data_col):#并发搜索
        g = [self.pgevent.spawn(self.get_url, data) for data in data_col]
        print (len(g))
        gevent.joinall(g)
        return g

    def save_summary_related(self,parse_article_summary, related_search, rid):  # 保存从数据库中提取的摘要与百度摘要，和搜索关键词
        try:
            related_list =""
            for related in related_search:
                related_list = "|".join([related_list,related])
            tmp = {}
            tmp["Article_RID"] = rid
            tmp["Article_Summary"] = parse_article_summary
            tmp["Baidu_Related_list"] =related_list
            self.db_obj.insert_summary_related(tmp) # 将从文章提取的摘要插入数据库
        except:
            pass

    def tf_idf(self, res1=None, res2=None):
        # 向量，可以使用list表示
        vector_1 = []
        vector_2 = []
        # 词频，可以使用dict表示
        tf_1 = {i[0]: float(i[1]) for i in res1}
        tf_2 = {i[0]: round(i[1]) for i in res2}

        res = set(list(tf_1.keys()) + list(tf_2.keys()))
        # 填充词频向量
        for word in res:
            if word in tf_1:
                vector_1.append(tf_1[word])
                if word in tf_2:
                    vector_2.append(tf_2[word])
                else:
                    vector_2.append(0)
            else:
                vector_1.append(0)
                if word in tf_2:
                    vector_2.append(tf_2[word])
        return vector_1, vector_2

    def numerator(self, vector1, vector2):
        # 分子
        return sum(a * b for a, b in zip(vector1, vector2))

    def denominator(self, vector):
        # 分母
        return math.sqrt(sum(a * b for a, b in zip(vector, vector)))

    def run(self, vector1, vector2):
        try:
            res = self.numerator(vector1, vector2) / (self.denominator(vector1) * self.denominator(vector2))
        except:
            res = 0
        return res

    def cut_word(self, article):
        # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
        res = jieba.analyse.extract_tags(
            sentence=article, topK=20, withWeight=True, allowPOS=('n',))
        return res

    def run(self,task_id):#本地文章与百度文章进行比对
        self.db_obj.db_obj.select_article_data()
        search_all_url=  self.crawl_keys_url(data_col)#获取搜索结果的若干页url
        """
        for i in search_all_url:
            tmp = i.get()
            if tmp:
                print (tmp[0])
                for _ in tmp[0]:
                    print (_)
                print (len(tmp[0]))
                print (tmp[1])
"""

        a = self.crawl_url(search_all_url)#并发去访问所有页面

if __name__ == '__main__':
    t = Baidu_compare()
    #data_col = t.select_compare_Article_List()
    data_col = [(1,'肝脏','点点滴滴娃娃去去去顶顶顶顶顶烦烦烦v'),(2,'肺病','顶顶顶哒哒哒哇哇哇啦啦啦了了了了了顶顶顶顶')]

    data_col = t.db_obj.select_article_data()
    t.find_max_similar(data_col)
