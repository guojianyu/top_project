#该脚本是对数据操作的封装

from pymongo import MongoClient
import pymongo
from gridfs import *
from bson import ObjectId


#为客户端的任务表和就绪表添加必要的索引
#conn = MongoClient(setting.DATABASES_IP, 27017, connect=False)
#db = conn[setting.DATABASES]  # 存储任务队列，任务队列数据库
#tb = db[setting.TASKS_LIST]
#为总任务列表建立guid的索引，和guid,topic的联合索引
#tb.create_index(setting.ROW_GUID, unique=False)
#tb.create_index([(setting.ROW_GUID, DESCENDING), (setting.ROW_TOPIC, DESCENDING)])#

#为就绪任务列表建立guid的索引，和guid,topic的联合索引
"""
for topic in setting.TOPIC:
    db[topic + setting.READY_LIST].create_index(setting.ROW_GUID, unique=False)
    db[topic + setting.READY_LIST].create_index([(setting.ROW_GUID, DESCENDING), (setting.ROW_TOPIC, DESCENDING)])#为就绪链表创建联合唯一索引

"""
class collection_db:
    def __init__(self):
        conn = MongoClient('127.0.0.1', 27017, connect=False)
        self.db = conn['Baidu_Search']  # 存储任务队列，任务队列，超时队列数据库
        self.tb = self.db['Article_list']  # 保存数据的数据库

    def find_data(self,data,limit=0):#查找数据,可以指定得到前几行
        return self.tb.find(data).limit(limit)


if __name__ == '__main__':
    obj = collection_db()
    #obj.insert_data(obj.tb,{'a':1,'b':2(crawl)})
    a = obj.find_data(obj.tb,{'isFind':0})
    for i in a:
        #print (i)
        i['auto_clean_data'] = 3
        obj.update_clx_data(obj.tb,{'_id':i['_id']},i)
