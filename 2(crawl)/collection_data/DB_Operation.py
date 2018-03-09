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
        conn = MongoClient('192.168.5.10', 27000)
        self.db = conn['Crawl_Task']  # 存储任务队列，任务队列，超时队列数据库
        self.tb = self.db['Crawl_Task_Rule']  # 保存数据的数据库
        self.coll_tb = conn['Collection_Data']['collection_all_data']#存储所有聚合任务的结果
        self.coll_task = conn['Collection_Data']['collection_all_task']#存储所有聚合任务
    def scan_group_task(self):
        task = self.coll_task.find_and_modify(
            query={"Task_Status":0}, update={"$set":{"Task_Status":1}},)
        return task

    def save_group_result(self,data):
        self.coll_tb.insert(data)
    def update_task_status(self,_id,Task_Status=2):
        self.coll_task.update({"_id":_id},{"$set": {"Task_Status": 2}})

    def group_task_data(self,match={}):#得到聚合结果
        if match:
            return self.tb.aggregate([match,{"$group":{"_id":"$Article_Keyword","count":{"$sum":1}}},{"$match":{"count": {"$gt": 1 } }}],allowDiskUse= True)
        else:
            return self.tb.aggregate([{"$group": {"_id": "$Article_Keyword", "count": {"$sum": 1}}}, {"$match": {"count": {"$gt": 1}}}],allowDiskUse=True)

if __name__ == '__main__':
    obj = collection_db()
    #a = obj.select_forbidden_words()
    a  = obj.test()
    print (a)
