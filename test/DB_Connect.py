import pymssql
class task_opt():
    def __init__(self):
        DB_DICT = {
            'server': '192.168.1.33',
            #'server': '192.168.0.8',
            'user': 'sa',
            'password': 'Q!W@E#R$T%2015q1w2e3r4t5',
            'database': 'Crawl_Task'
        }
        self.db_obj =SqlRW(**DB_DICT)#实例化数据库对象

    def insert_data(self, data):  # 自身比较
        sql = "insert into Article_List_1(QID,Article_Title,Article_Descr,Article_Keywords,Article_Path,Article_Content,Article_Note,Article_fromURL,Article_CateID,Article_GroupID,Task_RID) VALUES (%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r);" % (
            data["_id"], data["Rule_Match_T"][:300], data["Rule_Match_D"][:300], data["Rule_Match_K"][:300],
            data["Rule_Match_P"][:300], data["Rule_Match_Cs"]
            , data["Article_Keyword"], data["Rule_URL"], data["Cate_CID"], data["Cate_FID"], data["Task_RID"]
        )
        self.db_obj.WriteSql(sql)
        return sql

    def select_GXB_News_List(self):
        Sql_info = 'select * from GXB_News_List;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def select_GXB_Cate(self):#表中右重复栏目
        Sql_info = 'select MIN(RID),Cate_Name from GXB_Cate WHERE isDelete=0 GROUP BY Cate_Name;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def select_sitive_word(self):
        Sql_info = 'select Word_Name from BadWords WHERE Word_Type=0;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def insert_crawl_task(self,Task_URL,Task_On_rule,Task_Out_rule,Task_Deep,Task_Match_field,Task_Match_rule,Task_isClear,Task_Level):
        sql = "insert into Crawl_Task(Task_URL,Task_On_rule,Task_Out_rule,Task_Deep,Task_Match_field,Task_Match_rule,Task_isClear,Task_Level) VALUES (%r,%r,%r,%r,%r,%r,%r,%r);" % (
            Task_URL, Task_On_rule, Task_Out_rule, Task_Deep, Task_Match_field, Task_Match_rule,Task_isClear,Task_Level)
        self.db_obj.WriteSql(sql)
    def update_single_crawl_task(self,rid):
        sql = "update Crawl_Task set Task_Status=0  WHERE RID=%r;" % (rid)
        self.db_obj.WriteSql(sql)

    def select_all_crawl_task(self):
        Sql_info = 'select RID from Crawl_Task;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def select_crawl_task(self):
        Sql_info = 'select RID,Task_Name,Task_URL,Task_Status,Creat_Date,Task_Level from Crawl_Task ORDER by Task_Status ASC ;'  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def delete_crawl_task(self):#清除
        Sql_info = 'delete from Crawl_Task;'  #
        self.db_obj.WriteSql(Sql_info)
    def delete_sigle_task(self,id):
        Sql_info = 'delete from Crawl_Task WHERE RID=%r;'%(id)
        self.db_obj.WriteSql(Sql_info)

    def insert_Crawl_Status(self,Task_RID,Task_PID,StatusID):#任务开始执行时调用该接口，插入记录任务执行情况任务表，用于用户停止任务杀死进程
        sql = "insert into Crawl_Status(Task_RID,Task_PID,StatusID) VALUES (%r,%r,%r);" % (
            Task_RID, Task_PID, StatusID)
        self.db_obj.WriteSql(sql)
    def stop_Crawl_Status(self,rid,flag=1):#暂停任务,将中间临时表的状态更改为暂停
        sql = "update Crawl_Status set StatusID= %r  WHERE Task_RID=%r;" % (flag, rid)
        self.db_obj.WriteSql(sql)

    def start_Crawl_Status(self,rid,flag=0):#将任务状态更改为可被执行状态0
        sql = "update Crawl_Task set Task_Status= %r  WHERE RID=%r;" % (flag, rid)
        self.db_obj.WriteSql(sql)


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
    #t.delete_crawl_task()

    a = t.look_crawl_site()
    print (a)





