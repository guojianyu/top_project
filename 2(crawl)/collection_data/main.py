import DB_Operation
import datetime
from bson.objectid import ObjectId

class collection_task:
    def __init__(self):
        self.obj = DB_Operation.collection_db()
    def crate_object_id(self,year,month,day):
        gen_time = datetime.datetime(year,month,day)
        dummy_id = ObjectId.from_datetime(gen_time)
        return dummy_id

    def scan_task(self):#得到需要执行的聚合任务
        task  = self.obj.scan_group_task()
        return task
    def group_data(self,task_id,condition):
        data = self.obj.group_task_data(condition)
        try:
            for item in data:
                try:
                    item["Task_ID"] = task_id
                    self.save_group_result(item)
                except:
                    pass
        except:
            pass
    def save_group_result(self,data):
        self.obj.save_group_result(data)
    def run(self):
        while True:
            task = self.scan_task()#获取任务
            if not task:
                continue
            print (task)
            if task["Task_Type"] == 1:
                _start = [int(item) for item in task["Start_Time"].split("-")]
                _end = [int(item) for item in task["End_Time"].split("-")]
                _start_id = self.crate_object_id(_start[0],_start[1],_start[2])
                _end_id = self.crate_object_id(_end[0],_end[1],_end[2])
                print (_start_id)
                print (_end_id)
                match = {"$match":{"_id":{"$gte":_start_id,"$lte":_end_id}}}
            else:
                match = {}
            task_id = task["_id"]
            self.group_data(str(task_id),match)#聚合
            self.obj.update_task_status(task_id,2)#更新为完成状态
if __name__ == "__main__":
    a = collection_task()
    a.run()