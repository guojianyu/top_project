import pymssql
import json
class task_opt():
    def __init__(self):
        DB_DICT = {
            'server': '192.168.5.33',
            'user': 'sa',
            'password': 'Q!W@E#R$T%2015q1w2e3r4t5',
            'database': 'Crawl_Task'
        }

        self.db_obj =SqlRW(**DB_DICT)#实例化数据库对象

    def select_crawl_task(self):#最多获取6个任务
        Sql_info = 'select top 6 Task_URL,Task_On_rule,Task_Out_rule,Task_Deep,Task_Match_field,Task_Match_rule,Task_isClear,RID from Crawl_Task WHERE (Task_Status=0 ) ORDER BY Task_Level DESC ;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def update_ctask_status(self,id,flag=1):#更新爬虫任务状态
        sql = "update Crawl_Task set Task_Status= %r WHERE RID=%r;"%(flag,id)
        self.db_obj.WriteSql(sql)

    def delete_crawl_task(self):
        Sql_info = 'delete from Crawl_Task;'# 根据任务ID得到具体任务信息
        self.db_obj.WriteSql(Sql_info)

    def insert_Crawl_Status(self, Task_RID, Task_PID, StatusID=0):  # 任务开始执行时调用该接口，插入记录任务执行情况任务表，用于用户停止任务杀死进程
        sql = "insert into Crawl_Status(Task_RID,Task_PID,StatusID) VALUES (%r,%r,%r);" % (
            Task_RID, Task_PID, StatusID)
        self.db_obj.WriteSql(sql)

    def select_stop_Crawl_Status(self):  #查询中间表被暂停的任务
        sql = "select * from Crawl_Status WHERE StatusID=1;"
        result = self.db_obj.ReadSql(sql)
        return result

    def delete_Crawl_Status(self,rid):
        Sql_info = 'delete from Crawl_Status WHERE Task_RID=%r ;'%(rid)  # 根据任务ID得到具体任务信息
        self.db_obj.WriteSql(Sql_info)

    def init_crawl_task(self):#脚本运行前动作，将中间表清空，将运行状态的任务和就绪态的任务更改为初始态
        Sql_info = 'delete from Crawl_Status;' #清空中间表
        self.db_obj.WriteSql(Sql_info)
        sql = "update Crawl_Task set Task_Status= 0  WHERE Task_Status=1 or Task_Status=2;"#将就绪态和执行态值为初始态
        self.db_obj.WriteSql(sql)

    def insert_Crawl_Task_Rule(self,Task_RID, Rule_Domain, Rule_URL, Rule_Match_T, Rule_Match_D, Rule_Match_K,
                               Rule_Match_P, Rule_Match_C,Rule_Match_Cs):  # 将匹配结果写入数据库
        sql = "insert into Crawl_Task_Rule(Task_RID,Rule_Domain,Rule_URL,Rule_Match_T,Rule_Match_D,Rule_Match_K,Rule_Match_P,Rule_Match_C,Rule_Match_Cs) VALUES (%r,%r,%r,%r,%r,%r,%r,%r,%r);" % (
            Task_RID, Rule_Domain, Rule_URL, Rule_Match_T, Rule_Match_D,Rule_Match_K, Rule_Match_P, Rule_Match_C,Rule_Match_Cs)

        #print (sql)
        self.db_obj.WriteSql(sql)

    def check_url_Rule(self,Rule_URL,Task_RID):
        sql = "select RID from Crawl_Task_Rule WHERE Task_RID=%r AND Rule_URL=%r;"%(Task_RID,Rule_URL)
        result = self.db_obj.ReadSql(sql)
        return len(result)

    def clear_url_Rule(self,Task_RID):
        Sql_info = 'delete from Crawl_Task_Rule WHERE Task_RID=%r;'%(Task_RID)  # 清空中间表
        self.db_obj.WriteSql(Sql_info)

    def update_aaactask_status(self,flag=0):  # 更新爬虫任务状态
        sql = "update Crawl_Task set Task_Status=%r WHERE Task_Level=0;" % (flag)
        self.db_obj.WriteSql(sql)

    def test(self):
        sql = "select COUNT(*) from Crawl_Task;"
        result = self.db_obj.ReadSql(sql)
        return result

    def test1(self):
        Sql_info = 'select Task_URL,Task_On_rule,Task_Out_rule,Task_Deep,Task_Match_field,Task_Match_rule,Task_isClear,RID from Crawl_Task WHERE (RID=121);'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

class SqlRW(object):
    def __init__(self, server, user, password, database):
        self.server = server
        self.user = user
        self.password = password
        self.database = database

    def __GetConnect(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database)
        cursor = self.conn.cursor()
        if not cursor:
            print ('connected failed')
        return cursor

    def ReadSql(self,sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def WriteSql(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        self.conn.commit()
        return 1

    def close_connect(self):
        self.conn.close()

if __name__ == "__main__":
    t = task_opt()
    #t.update_aaactask_status()
    print (t.test())
    #248088
    #a = t.test1()
    #print (a)
    #t.init_crawl_task()
    #t.delete_crawl_task()
    #a = t. select_crawl_task()[0]
    #print (type(a))
    #print (a)
    """
    for i in a:
        print (i)
        Task_URL = i[0]
        Task_On_rule= i[1]
        Task_Out_rule =i[2]
        Task_Deep =i[3]
        Task_Match_field =i[4]
        Task_Match_rule =i[5]
        #print (Task_URL,Task_On_rule,Task_Out_rule,Task_Deep,Task_Match_field,Task_Match_rule)
        print (Task_Match_field)
        print (Task_Match_rule)
        print (Task_Match_rule.replace('\\"','"'))
        print (json.loads(Task_Match_rule.replace('\\"','"')))
    """
