
from fake_useragent import UserAgent
import requests
import json
import time
import hashlib
import execjs
import math
ua = UserAgent()
class Crawl_Toutiao:
    def __init__(self):
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': ua.random
        }
    def crawl_toutiao_keyword(self,keyword):#爬取搜索结果的所有url及其用户id和用户名
        all_data_list = []
        offset = 0
        while True:
            url = 'https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=%s&autoload=true&count=20&cur_tab=1&from=search_tab'%(offset,keyword)
            wbdata = requests.get(url).text
            wbdata = json.loads(wbdata)
            if not wbdata["return_count"]:
                return all_data_list
            for item in wbdata["data"]:
                try:
                    """
                    print (item["media_creator_id"])#头条号id
                    print (item["media_name"])#头条号名字
                    print (item["title"])
                    print (item["article_url"])#文章url
                    """
                    all_data_list.append({"Article_User_Id":item["media_creator_id"],"Article_User_name":item["media_name"],
                                          "Artilce_Url":item["article_url"],"Artilce_Title":item["title"]})
                except:
                    pass
            offset +=20

    def getASCP(self):
        t = int(math.floor(time.time()))
        e = hex(t).upper()[2:]
        m = hashlib.md5()
        m.update(str(t).encode(encoding='utf-8'))
        i = m.hexdigest().upper()

        if len(e) != 8:
            AS = '479BB4B7254C150'
            CP = '7E0AC8874BB0985'
            return AS, CP
        n = i[0:5]
        a = i[-5:]
        s = ''
        r = ''
        for o in range(5):
            s += n[o] + e[o]
            r += e[o + 3] + a[o]

        AS = 'A1' + s + e[-3:]
        CP = e[0:3] + r + 'E1'
        return AS, CP

    def crawl_toutiao_user(self,AS,CP):

        url = "https://www.toutiao.com/c/user/article/?page_type=1&user_id=3902939306&max_behot_time=1519973210&count=20&as=%s&cp=%s&_signature=rFNpgBAT9t5iOO9S0URV96xTaZ"%(AS,CP)
        wbdata = requests.get(url,headers=self.headersParameters).text
        print (wbdata)

    def get_signature(self, user_id):
        """
        计算_signature
        :param user_id: user_id不需要计算，对用户可见
        :return: _signature
        """
        req = requests.Session()
        # js获取目的
        jsurl = 'https://s3.pstatp.com/toutiao/resource/ntoutiao_web/page/profile/index_8f8a2fb.js'
        resp = req.get(jsurl, headers=self.headersParameters)
        js = resp.text
        effect_js = js.split("Function")
        js = 'var navigator = {};\
           navigator["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36";\
        ' +  "function" + effect_js[3] + "function" + effect_js[4] + "function result(){ return TAC.sign(" + user_id + ");} result();"
        js1 = "function" + effect_js[3]
        print (js)
        vl5x = execjs.eval(js)
        print  (vl5x)
        return vl5x





if __name__ == "__main__":
    keyword = "健康"
    obj = Crawl_Toutiao()
    AS,CP = obj.getASCP()
    #obj.crawl_toutiao_user(AS,CP)
    obj.get_signature("11111")