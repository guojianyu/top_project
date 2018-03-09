
import itertools
import urllib
import requests
import os
import re
import sys
import random
import uuid
from gevent import monkey,pool; monkey.patch_socket()
import gevent
from fake_useragent import UserAgent
ua = UserAgent()


str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2(crawl)': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2(crawl)',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2(crawl)&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    print ('image')
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return res.url


def mkDir(doc,dirName):
    dirpath = os.path.join(sys.path[0],doc,dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath
def mkdocDir(doc):
    dirpath = os.path.join(sys.path[0],doc)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def crawl_image(url):
    try:
        html = requests.get(url, timeout=1).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        print ('jayguo.txt:',len(imgUrls))
        if len(imgUrls) == 0:  # 没有图片则结束
            print('end:',url)
            return 'end'
        return imgUrls
    except:
        return 'request_error'


pgevent = pgevent = pool.Pool(100)
def batch_get_url(urls):
    print('start')
    g = [pgevent.spawn(crawl_image,url) for url in urls]
    gevent.joinall(g)
    return g

def run(doc,word):
    print (word)
    print("=" * 50)
    all_image_url = []
    dirpath = mkDir(doc,word)
    quit_flag = 0
    urls = buildUrls(word)
    crawl_url = []
    count = 0
    for url in urls:
        if count < 6000:
            count += 1
            crawl_url.append(url)
        else:
            result = batch_get_url(crawl_url)
            for item in result:
                tmp = item.get()
                if (type(tmp) == list):
                    all_image_url.extend(tmp)
                if tmp == 'end':
                    print('搜索完成')
                    quit_flag = 1
                    break
            if quit_flag:
                break
            count = 0
            crawl_url = []
    print('all_end')
    true_all_url = []
    g = [pgevent.spawn(downImg, url, dirpath, str(uuid.uuid1()) + '.jpg') for url in all_image_url]
    gevent.joinall(g)
    for i in g:
        image_url = i.get()
        if image_url:
            true_all_url.append(image_url)
    print('总计获得url:', len(list(set(true_all_url))))
    with open('fei_url_collection', "a") as f:
        tmp = word + ':' + str(true_all_url)
        f.write(tmp)
        f.write('\n')
    print('结束')

if __name__ == '__main__':

    doc_list =['肿瘤','肺癌','肝癌','白血病','乳腺癌','胰腺癌','食道癌','胃癌','肠癌','甲状腺癌','子宫癌',
          '前列腺癌','鼻咽癌','口腔癌','皮肤癌','卵巢癌','膀胱癌','肾癌','胆囊癌',
          '淋巴瘤','肉瘤','骨肿瘤','脑肿瘤','男科'
          ]

    words_list = [
                ['肿瘤','癌症','肿瘤细胞','癌症细胞'],
                ['肺癌','肺','咳嗽'],
                ['肝癌','肝'],
                ['白血病','白细胞','孩子'],
                ['乳腺癌','乳房'],
                ['胰腺癌'],
                ['食道癌','食道','食管','喉咙通'],
                ['胃癌','胃'],
                ['肠癌','肠道'],
                ['甲状腺癌','甲状腺'],
                ['子宫癌','女性'],
                ['前列腺癌','男性'],
                ['鼻咽癌',],
                ['微笑',],
                ['晒太阳',],
                ['卵巢癌',],
                ['膀胱癌','腹部疼'],
                ['肾癌','肾','腰疼'],
                ['胆囊癌',],
                ['淋巴瘤','淋巴癌'],
                ['肉瘤',],
                ['骨癌','骨肿瘤','关节疼'],
                ['脑癌','大脑'],
                ['男人',]
                ]
    """
    doc_list = ['肝病','肝硬化','肝炎','脂肪肝','酒精肝','糖尿病','高血压','冠心病','慢阻肺',
                '哮喘','帕金森','阿尔兹海默','胃炎','纤维化'
                ]

    words_list=[['肝',],['喝酒',],['肝炎病毒',],['肥胖',],
                ['喝酒',],['糖尿病',],['高血压',],['冠心病',],
                ['呼吸+大自然',],['哮喘',],['帕金森','老人'],
                ['阿尔兹海默','老年痴呆','老人'],
                ['暴饮暴食',],
                ['纤维化',],
                ]
    """
    doc_list =['肠病','干细胞','健康']
    words_list=[['肠病',],['干细胞',],['运动',]]
    print (len(doc_list))
    print (len(words_list))
    for count,doc in enumerate(doc_list):
        mkdocDir(doc)
        for word in words_list[count]:
            run(doc, word)

