import DB_Connect,DB_Operation
import xlwt
from datetime import datetime
book = xlwt.Workbook(encoding='gbk', style_compression=0)
sheet = book.add_sheet('auto_clean_data', cell_overwrite_ok=True)
DBOPT_OBJ = DB_Connect.task_opt()  # 操作数据库对象
Mongo_obj = DB_Operation.collection_db()
rule_coll = DBOPT_OBJ.select_crawl_task()

dict = {'split':[],'replace':[],"Task_RID":3000,"Task_Status":0,"Task_URL":"","Creat_Date":datetime.now(),"Task_Level":1,"Task_Type":0}

all_ok = DBOPT_OBJ.select_all_crawl_task()
for item in all_ok:
    data_coll = Mongo_obj.select_task_sum(item[0])
    if data_coll >100:
        dict["Task_RID"] = item[0]
        dict["Task_URL"] =item[1]
        Mongo_obj.insert_data(dict)
        dict.pop("_id")
        pass
