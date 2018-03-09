import DB_Operation,DB_Connect
import re
import math
import time
from bson.objectid import ObjectId
import jieba.analyse
class clean_data:
    def __init__(self):
        self.db_obj = DB_Operation.collection_db()
        self.sql_obj = DB_Connect.task_opt()
    def cut_word(self,article):
        # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
        res = jieba.analyse.extract_tags(
            sentence=article, topK=20, withWeight=True, allowPOS=('n',))
        return res


    def run(self):
        while True:
            try:
                data = self.db_obj.test()
                if data:
                    data["_id"] = str(data["_id"])
                    sql = self.sql_obj.insert_data(data)
                else:
                    time.sleep(1)
            except Exception as e:
                #print (data["_id"])
                #print (sql)
                try:
                    self.db_obj.update_data_flag(ObjectId(data["_id"]))
                except:
                    pass
                #print (e)

if __name__ == "__main__":
    obj = clean_data()
    obj.run()



