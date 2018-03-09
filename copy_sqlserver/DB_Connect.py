#B D ok
import pymssql,datetime,random
class task_opt():
    def __init__(self):
        DB_DICT = {
            'server': '192.168.1.33',
            'user': 'sa',
            'password': 'Q!W@E#R$T%2015q1w2e3r4t5',
            # 'database': 'TOPTHEALTH2017'
            'database': 'Crawl_Task'
        }
        self.db_obj =SqlRW(**DB_DICT)#实例化数据库对象


    def select_rule_List(self,max_id):#自身比较
        Sql_info = "select top 600 * from Crawl_Task_Rules WHERE (RID>%r) ORDER BY RID ASC ;"%(max_id) #根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def update_Article_flag(self,id,flag=1):
        sql = "update Article_list set isFind= %r  WHERE RID=%r;" % (flag, id)
        print(sql)
        self.db_obj.WriteSql(sql)

    def look_biao(self):
        Sql_info = "select COUNT (RID) from Article_List WHERE isFind =1;"  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def get_max_rid(self):
        Sql_info = "select top 1 * from Crawl_Task_Rules WHERE (copy_flag =1) ORDER BY RID DESC ;"  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def update_ctask_status(self, id, flag=1):  # 更新爬虫任务状态
        sql = "update Crawl_Task_Rules set copy_flag= %r WHERE RID=%r;" % (flag, id)
        self.db_obj.WriteSql(sql)

class SqlRW(object):
    def __init__(self, server, user, password, database):
        self.server = server
        self.user = user
        self.password = password
        self.database = database

    def __GetConnect(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database,charset='utf8')
        cursor = self.conn.cursor()
        if not cursor:
            print ('connected failed')
        return cursor


    def ReadSql(self,sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.close()
        return result

    def WriteSql(self, sql):
        cursor = self.__GetConnect()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        return 1

if __name__ == "__main__":
    import time
    t = task_opt()
  #  肝脏:0.23 | 护肝:0.07 | 肝炎:0.06 | 酒精:0.05 | 维生素:0.05 | 肝细胞:0.05 | 食物:0.05 | 解毒:0.05 | 作用:0.04 | 肝病:0.04 | 可以:0.04 | 修复:0.03 | 解酒:0.03 | 蛋白质:0.03 | 功效:0.03 | 养肝护:0.03 | 养肝:0.03 | 功能:0.03 | 代谢:0.03 | 药物:0.03 | ',)
    #t.delt_crawl_info()
    a = t.get_max_rid()
    print (a)
    #print (t.look_biao())
    #print (t.look())
    """
    start_time = time.time()
    start_len = len(t.look_biao())
    while True:
        if time.time()-start_time >=60:
            start_time = time.time()
            end_len = len(t.look_biao())
            print ('1分钟比对个数：',end_len-start_len)
            start_len = end_len
    """







