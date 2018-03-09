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
        self.tt = self.db["auto_clean_data"]
        self.tb = self.db['Crawl_Task_Rule']  # 保存数据的数据库
        self.clear_tb  = self.db['Clear_Task']#保存解析任务的数据表
        self.finish_tb = self.db["Finish_Data"]#保存清洗完成的数据
        self.forbidden_tb = self.db["Forbidden_Words"]#违禁词库
        self.class_tb = self.db["Site_Cate_Rules"]#存储归类信息的数据表
    def insert_data(self,data):#插入清洗数据库
        self.clear_tb.insert(data)

    def select_clear_task(self):#查找清洗数据的任务，任务状态为0,改为状态为1的执行中
        return self.clear_tb.find_and_modify(
            query={"Task_Status":0}, update={"$set":{"Task_Status":1}})
    def update_task_finish(self,id,Task_Status=3):
        return self.clear_tb.update({"_id": id}, {"$set": {"Task_Status": Task_Status}})
    def select_task_data(self,Task_RID):#得到该任务要清洗的数据
        return self.tb.find({"Task_RID":Task_RID,"flag":0})
    def delete_repeat_data(self,_id):#删除数据库中的重复文章数据
        return self.tb.remove({"_id":_id})

    def update_data_clean(self,id):#更新待清洗数据为清洗完成状态
        return self.tb.update({"_id":id},{"$set":{"flag":1}})
    def save_finish_data(self,data):#将清洗的数据保存
        self.finish_tb.insert(data)
    def select_forbidden_words(self):#查询违禁词库
        return self.forbidden_tb.distinct("forbidden_word")

    def select_allclass_conditions(self):#获取归类信息
        result_info = []
        all_info = self.class_tb.find({},{"_id":0}).sort([("Rules_Order",1)])
        for item in all_info:
            result_info.append(item)
        return result_info

    def test(self,data):
         return self.tt.insert(data)

if __name__ == '__main__':
    obj = collection_db()
    #a = obj.select_forbidden_words()
    #print (a)
    a  = obj.test()
    print (a)
