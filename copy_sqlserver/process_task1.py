#扫描数据库，提取有用数据
import time
from multiprocessing import Process,Queue
import DB_Connect,db_oprate

mongo_obj = db_oprate.collection_db()
sql_obj = DB_Connect.task_opt()
class filter:
    def __init__(self):
        pass

    def sacn_add_task(self, myqueue):  # 获取任务的进程，获取的任务添加到队列
        result = sql_obj.get_max_rid()
        if result:
            max_rid = result[0][0]
        else:
            max_rid = 0
        print ("最大id:",max_rid)
        while True:
            try:
                if myqueue.qsize() <= 0:
                    data_list= sql_obj.select_rule_List(max_rid)
                    if data_list:
                        myqueue.put(data_list)
                        max_rid = data_list[-1][0]
                    else:
                        print ("没有数据了")
                        time.sleep(1)
            except Exception as e:
                print (e)

    def copy_sql_mongo(self,data):
        tmp_dict = {}
        tmp_dict['Task_RID'] = data[1]
        tmp_dict['Rule_Domain'] = data[2]
        tmp_dict['Rule_URL'] = data[3]
        tmp_dict['Rule_Match_T'] = data[4]
        tmp_dict['Rule_Match_D'] = data[5]
        tmp_dict['Rule_Match_K'] = data[6]
        tmp_dict['Rule_Match_P'] = data[7]
        tmp_dict['Rule_Match_C'] = data[9]
        tmp_dict['Rule_Match_Cs'] = data[10]
        tmp_dict['flag'] = 0
        tmp_dict['Article_Keyword'] = 0
        tmp_dict['Article_Keywords'] = 0
        tmp_dict['Article_Keywords_3'] = 0
        return tmp_dict

    def sql_copy_mongo(self,data_col):

        for item in data_col:
            try:
                #print (item)
                tmp = self.copy_sql_mongo(item)
                #print (tmp)
                mongo_obj.insert_data(tmp)
            except Exception as e:
                print('出错:',e)
        sql_obj.update_ctask_status(item[0])

    def excutor_task(self,myqueue):#执行任务
        while True:
            try:
                result = myqueue.get()
                print ('得到任务：')
                self.sql_copy_mongo(result)
            except Exception as e:
                print('执行任务异常：',e)

    def run(self):
        tmp_list = []
        myqueue = Queue()
        tmp_list.append(Process(target=self.sacn_add_task, args=(myqueue,)))
        for _ in range(6):  # 开启6个进程
            p = Process(target=self.excutor_task, args=(myqueue,))  # 执行任务的进程
            tmp_list.append(p)
        for item in tmp_list:
            item.start()
        for item in tmp_list:
            item.join()

if __name__ =="__main__":
    obj = filter()
    obj.run()
