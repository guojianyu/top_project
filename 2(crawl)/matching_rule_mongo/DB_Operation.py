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
        self.tb = self.db['Crawl_Task_Rule']  # 保存爬取数据的数据表
        self.task_tb = self.db['Crawl_Task'] #保存爬取规则的数据表
        self.status_tb = self.db['Crawl_Status']#通知停止任务中间表，重启清空

    def insert_data(self,data):#插入数据库
        self.tb.insert(data)

    def find_modify(self,query,update,upsert=False):#原子性操作查找并修改状态
        return self.task_tb.find_and_modify(
                query=query, update=update,upsert=upsert)

    def init_crawl_task(self):
        self.status_tb.remove()#清空中间表
        self.much_update_data(self.task_tb,{"Task_Status":{'$in':[1,2]}},{"Task_Status":0})#将就绪状态和执行状态的任务置为初始状态

    def much_update_data(self, tb, query, update):  # 批量更新
        ret = tb.update(
            query,
            update,
            multi=True
        )
        return ret

    def select_stop_Crawl_Status(self,Device_DID):#查看暂停任务
        stop_tasks = self.status_tb.find({'StatusID':1,'Device_DID':Device_DID})#查找该设备号下的暂停任务
        return stop_tasks

    def insert_Crawl_Status(self,Task_RID, Task_PID,Device_DID,StatusID=0):#任务开始执行时调用该接口，插入记录任务执行情况任务表，用于用户停止任务杀死进程
        #1:任务ID，2(crawl)：绑定任务的进程ID 3：设备ID 4：是否暂定的标志
        self.status_tb.insert({'Task_RID':Task_RID,'Task_PID':Task_PID,'Device_DID':Device_DID,'StatusID':StatusID})

    def delete_Crawl_Status(self, Task_RID):#删除中间表的任务
        self.status_tb.remove({'Task_RID':Task_RID})

    def update_ctask_status(self, Task_RID, StatusID=1):#更改任务表的任务状态
        self.tb.update({'Task_RID': Task_RID},{'StatusID':StatusID})

    def test(self):
        return self.task_tb.find_one({'Task_Status':4})

if __name__ == '__main__':
    obj = collection_db()
    a =obj.test()
    print (a)
