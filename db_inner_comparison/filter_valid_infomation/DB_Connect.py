#B D ok
import pymssql
class task_opt():
    def __init__(self):
        DB_DICT = {
            'server': '192.168.1.65',
            'user': 'sa',
            'password': 'Q!W@E#R$T%2015q1w2e3r4t5',
            #'database': 'TOPTHEALTH2017'
            'database': 'DBS_Articles'
        }
        self.db_obj =SqlRW(**DB_DICT)#实例化数据库对象

    def look1(self):
        Sql_info = "select  top 100 Article_Keywords_3 from Article_CiPin GROUP BY Article_Keywords_3 HAVING  COUNT (Article_Keywords_3) >10;" #根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def look(self,cipin):
        Sql_info = "select  * from Article_CiPin WHERE Article_Keywords_3 =%r;"%(cipin)  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def look_biao(self):
        Sql_info = "select count(Article_Note) from Article_List WHERE isUse=1 GROUP BY Article_Note ;" # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def test(self):
        Sql_info = "select count(Article_Note) from Article_List WHERE isUse=1;"  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

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
  # 肝脏:0.23 |护肝:0.07 |肝炎:0.06 |酒精:0.05 | 维生素:0.05 | 肝细胞:0.05 | 食物:0.05 | 解毒:0.05 | 作用:0.04 | 肝病:0.04 | 可以:0.04 | 修复:0.03 | 解酒:0.03 | 蛋白质:0.03 | 功效:0.03 | 养肝护:0.03 | 养肝:0.03 | 功能:0.03 | 代谢:0.03 | 药物:0.03 | ',)
    #t.delt_crawl_info()
    start = time.time()
    #print (len(t.select_Article_List()))
    #print (len(t.look_biao()))
    print (t.test())
    #print (t.look1())
    print(time.time() - start)
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







