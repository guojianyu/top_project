#该脚本是对数据操作的封装

from pymongo import MongoClient
from gridfs import *
from bson import ObjectId
import setting

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
        conn = MongoClient(setting.DATABASES_IP, 27017, connect=False)
        self.db = conn[setting.DATABASES]  # 存储任务队列，任务队列，超时队列数据库
        self.tb = self.db[setting.DATA_DB] # 保存数据的数据库

    def choice_table(self,tb):#切换到就绪列表
        self.tb = self.db[tb]
        return self.tb

    def get_tb_count(self):#得到数据表的数据个数
        return self.tb.count()

    def insert_data(self,data):#插入数据库
        self.tb.insert(data)

    def del_data(self,data):#删除数据
        self.tb.remove(data)

    def update_clx_data(self,query,update):#提供条件更新数据, 有则更新没有则插入
        ret = self.tb.update(
            query,
            update,
            True
        )
        return ret

    def much_update_data(self,query,update):#批量更新
        ret = self.tb.update(
            query,
            update,
            multi=True
        )
        return ret

    def update_term_data(self,query,update): # 更改数据，根据条件，有则更新，没有则插入
        ret = self.tb.update(
            query,
            update,
            True
        )
        return ret

    def find_one(self,query):
        return self.tb.find_one(query)

    def find_data(self,data,limit=0):#查找数据,可以指定得到前几行
        return self.tb.find(data).limit(limit)

    def find_modify(self,query,update,upsert=False):#原子性操作
        return self.tb.find_and_modify(
                query=query, update=update,upsert=upsert)

    def find_modify_remove(self,query):#原子性操作，得到并删除
        return self.tb.find_and_modify(
                query=query, remove = True)

    def find_data_count(self,data={}): #得到查找数据的个数
        return  self.tb.find(data).count()

if __name__ == '__main__':
    obj = collection_db()
    #obj.insert_data(obj.tb,{'a':1,'b':2(crawl)})
    a = obj.find_data({'isFind':0})
    for i in a:
        #print (i)
        i['auto_clean_data'] = 3
        obj.update_clx_data({'_id':i['_id']},i)
