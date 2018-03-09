#该脚本是对数据操作的封装

from pymongo import MongoClient

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
        conn = MongoClient('192.168.1.10', 27000)
        self.db = conn['Crawl_Task']  # 存储任务队列，任务队列，超时队列数据库
        self.finish_tb = self.db["Finish_Data"]#保存清洗完成的数据
        self.summary_finish_tb = self.db["Finish_Data_Summary"]#保存清洗数据的摘要和相关搜索
        self.save_baidu =  conn['Baidu_Search']['Baidu_Search_Result']#存放百度搜索结果
        self.save_keyword_sentence = conn['Keyword_Sentence']['Keyword_Sentence']

    def insert_data(self,data):#插入百度搜索的文章
        self.save_baidu.insert(data)

    def insert_keyword_sentence(self,data):
        self.save_keyword_sentence.insert(data)

    def update_article_search(self,id,Baidu_Serach_Status):
        return self.finish_tb.update({"_id": id}, {"$set": {"Baidu_Serach_Status": Baidu_Serach_Status}})

    def select_article_data(self,id):#得到需要与百度进行搜索的文章
        return self.finish_tb.find({"Task_RID":id,"Baidu_Serach_Status":{"$exists":False}},{"_id":1,"Article_Keywords":1,"Article_Keyword":1,"Rule_Match_T":1,"Rule_Match_Cs":1}).limit(20)

    def insert_summary_related(self,data):
        self.summary_finish_tb.insert(data)

    def select_task_id(self):
        return self.finish_tb.distinct("Task_RID")
if __name__ == '__main__':
    obj = collection_db()
    #a = obj.select_forbidden_words()
    #print (a)
    a = obj.select_task_id()
    print (type(a))
    for i in a:
        print (i,type(i))
