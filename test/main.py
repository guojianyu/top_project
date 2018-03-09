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

    def record_keyword(self, content):
        data = self.cut_word(article=content)
        ci_tmp = ''
        ci_coll = ""
        for ci in data:
            ci_tmp = "".join([ci_tmp, ci[0], ":", str(round(ci[1], 2)), '|'])
            ci_coll = "".join([ci_coll, ci[0], '|'])
        return ci_tmp, ci_coll

    def run(self):
        a = self.sql_obj.select_all_crawl_task()
        for i in a:
            c = self.db_obj.test(i[0])
            if c ==0:
                self.sql_obj.update_single_crawl_task(i[0])


if __name__ == "__main__":
    obj = clean_data()
    obj.run()



