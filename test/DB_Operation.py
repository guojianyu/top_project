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
        self.tb = self.db['Crawl_Task_Rule']  # 保存数据的数据库
        self.test_tb = self.db["Clear_Task"]
    def insert_data(self,data):#插入清洗数据库
        self.test_tb.insert(data)
    def select_all_data(self):
        return self.test_tb.find()

    def select_clear_task(self):#查找清洗数据的任务，任务状态为0,改为状态为1的执行中
        return self.clear_tb.find_and_modify(
            query={"Task_Status":0}, update={"$set":{"Task_Status":1}})
    def update_task_finish(self,id):
        return self.clear_tb.update({"_id": id}, {"$set": {"Task_Status": 2}})

    def select_task_data(self):#得到该任务要清洗的数据
        return self.tb.find_and_modify(query={"flag": 2,"Article_Keyword":0},
                                   update={"$set": {"Article_Keyword": 0}})

    def update_data_clean(self,id,Article_Keyword):#更新待清洗数据为清洗完成状态
        return self.tb.update({"_id":id},{"$set":{"Article_Keyword":Article_Keyword}})

    def save_finish_data(self,data):
        self.finish_tb.insert(data)
    def insert_test_db(self,data):
        self.test_tb.insert(data)

    def select_task_sum(self,id):#查看任务ID下的任务总数
        return self.tb.find({"Task_RID":id}).count()

    def test(self,id):
        return self.tb.find({"Task_RID":id}).count()
if __name__ == '__main__':
    import time
    start = time.time()
    obj = collection_db()
    a = obj.select_task_data()
    for i in a:
        print (i)
    print ("总计用时：",time.time()-start)
