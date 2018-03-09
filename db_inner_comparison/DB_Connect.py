import pymssql
class task_opt():
    def __init__(self):
        DB_DICT = {
            'server': '192.168.1.69',
            'user': 'sa',
            'password': 'Q!W@E#R$T%2015q1w2e3r4t5',
            #'database': 'TOPTHEALTH2017'
            'database': 'DBS_Crawl'
        }

        self.db_obj =SqlRW(**DB_DICT)#实例化数据库对象
    def select_article_task(self,last_rid):#扫描任务
        Sql_info = "select top 1 RID from Article_list WHERE (goID<%r AND isDelete=0) ORDER BY RID ASC ;"%(last_rid)  # 根据任务ID得到具体任务信息
        print (Sql_info)
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def select_article_content(self,rid):
        Sql_info = "select  Article_Content from Article_list WHERE RID=%r;"%(rid)  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result[0]

    def select_article_center_content(self, min_rid,max_id):
        Sql_info = "select RID, Article_Content from Article_list WHERE RID>=%r AND RID<=%r;" % (min_rid,max_id)  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def insert_Article_CiPin(self, Article_RID, Article_Keywords, Article_Keywords_3, Article_Keyword):
        sql = 'insert into Article_CiPin(Article_RID,Article_Keywords,Article_Keywords_3,Article_Keyword) VALUES (%r,%r,%r,%r);' % (
            Article_RID, Article_Keywords, Article_Keywords_3, Article_Keyword
        )
        self.db_obj.WriteSql(sql)

    def update_Article_List(self, id):
        sql = "update Article_list_A set IsNote= 1 WHERE RID=%r;" % (id)
        print(sql)
        self.db_obj.WriteSql(sql)


    def select_Article_List(self,RID):#获取其他文章
        Sql_info = "select top 600 RID from Article_list WHERE (RID>%r AND isDelete=0) ORDER BY RID ASC ;"%(RID) #根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def update_Article_maxid(self,id,maxid):#记录任务id比对完成
        sql = "update Article_list set goID= %r  WHERE RID=%r;" %(maxid,id)
        self.db_obj.WriteSql(sql)

    def update_Article_delete(self,id,status=1):
        sql = "update Article_list set isDelete=%r WHERE RID=%r;"%(status,id)
        print (sql)
        self.db_obj.WriteSql(sql)

    def get_Maxrid_Article_List(self):
        Sql_info = "select  MAX (RID) from Article_list;" # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result[0][0]

    def look1(self):
        Sql_info = "select top 10000 * from Article_CiPin;"  # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result

    def look_biao(self):
        Sql_info = "select top 1 * from Article_list_D;" # 根据任务ID得到具体任务信息
        result = self.db_obj.ReadSql(Sql_info)
        return result
    def set_look_biao(self):
        sql = "update Article_list set goID=0 WHERE RID=1;"
        self.db_obj.WriteSql(sql)
    def look_delete_article(self):
        Sql_info = "select count(*)  from Article_list WHERE goID>0;"  # 根据任务ID得到具体任务信息
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
  #  肝脏:0.23 | 护肝:0.07 | 肝炎:0.06 | 酒精:0.05 | 维生素:0.05 | 肝细胞:0.05 | 食物:0.05 | 解毒:0.05 | 作用:0.04 | 肝病:0.04 | 可以:0.04 | 修复:0.03 | 解酒:0.03 | 蛋白质:0.03 | 功效:0.03 | 养肝护:0.03 | 养肝:0.03 | 功能:0.03 | 代谢:0.03 | 药物:0.03 | ',)
    #t.delt_crawl_info()
    #t.set_look_biao()
    print (t.look1())
   # print (t.look_delete_article())

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







