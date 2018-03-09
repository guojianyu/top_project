#获取任务后执行
import DB_Operation
import re
import math
import jieba.analyse
class clean_data:
    def __init__(self):
        self.db_obj = DB_Operation.collection_db()

    def cut_word(self,article):
        # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
        res = jieba.analyse.extract_tags(
            sentence=article, topK=20, withWeight=True, allowPOS=('n',))
        return res

    def record_keyword(self,content):
        data = self.cut_word(article=content)
        ci_tmp = ''
        ci_coll = ""
        for ci in data:
            ci_tmp = "".join([ci_tmp, ci[0], ":", str(round(ci[1], 2)), '|'])
            ci_coll = "".join([ci_coll, ci[0],'|'])
        return ci_tmp,ci_coll


    def Forbidden_word_filtering(self,content,Forbidden_word_all):#将文章中的违禁词去掉
        for word in Forbidden_word_all:
            try:
                word = str(word)
                content = content.replace(word,"")
            except:
                pass
        return content
    def Data_class_filtering(self,data,class_condition_all):#根据关键字进行数据归类
        result = ""
        for condition in class_condition_all:
            class_flag = 1
            Cate_Rules = condition["Cate_Rules"]
            for rule in Cate_Rules:
                if str(rule) not in data:
                    class_flag = 0
                    break
            if class_flag:#归类成功
                result = condition
                break
        return result

    def system_default_clean(self,content):#系统默认替换的信息字符串
        clean_date_match = '\d{0,4}[-/年]\d{0,2}[-/月]\d{0,2}[日]{0,1}'  # 数字时间去除
        clean_time_match = "\d{0,2}[:/时]\d{0,2}[:/分]\d{0,2}[秒]{0,1}"
        result = ''  # 替换成的结果
        content = re.sub(clean_date_match, result, content)
        content = re.sub(clean_time_match, result, content)
        content = content.strip()  # 去掉开头结尾空白符
        content = content.replace(" ", '')
        return content

    def content_split(self,content,split_rule):#内容截取
        if split_rule:
            re_math = '(?i)%s(.*)%s' % (split_rule[0], split_rule[1])
            result = re.findall(re_math,content, re.DOTALL)  # 匹配所有
            if not result:  # 没有匹配到结果
                result = content
            else:
                result = result[0]
        else:
            result = content
        return result

    def content_replace(self,content,replace_rule):#内容替换
        replace_rule = [replace_rule[i:i + 2] for i in range(0, len(replace_rule), 2)]
        for item in replace_rule:
            if len(item) !=2:
                continue
            content = content.replace(item[0], item[1])
        return content

    def get_clean_data(self,Task_RID):#得到该任务对应的所有数据
        return self.db_obj.select_task_data(Task_RID)

    def save_finish_data(self,data):
        self.db_obj.save_finish_data(data)

    def update_task_finish(self,_id):#更新任务为完成状态
        self.db_obj.update_task_finish(_id)

    def Forbidden_word_all(self):#获取全部违禁词
        return self.db_obj.select_forbidden_words()

    def update_single_data_clean(self,id):#更新单个数据清洗完成
        self.db_obj.update_data_clean(id)

    def get_allclass_conditions(self):#获取全部归类信息
        return self.db_obj.select_allclass_conditions()

    def delete_repeat_data(self,_id):#删除重复文章
        return self.db_obj.delete_repeat_data(_id)
    def run(self,task):
        split_rule = task['split']
        replace_rule = task['replace']
        Task_RID = task['Task_RID']
        _id = task["_id"]
        self.db_obj.update_task_finish(_id,2)
        try:
            if Task_RID.isdigit():
                Task_RID = int(Task_RID)
        except:
            pass
        while True:#防止远程数据库断连而无法执行任务
            try:
                Forbidden_word_all = self.Forbidden_word_all() #全部违禁词
                data_collection = self.get_clean_data(Task_RID)#该任务的全部数据
                class_condition_all = self.get_allclass_conditions()#全部归类信息
                for data in data_collection:
                    try:
                        data.pop("Rule_Match_C")
                        id = data.pop("_id")
                        title = data["Rule_Match_T"]#标题用于归类
                        content  = data["Rule_Match_Cs"]
                        content = self.system_default_clean(content)
                        content = self.Forbidden_word_filtering(content,Forbidden_word_all)
                        content = self.content_split(content,split_rule)
                        content = self.content_replace(content,replace_rule)
                        data["Rule_Match_Cs"] = content
                        data["Article_Keywords"],data["Article_Keyword"] = self.record_keyword(content)
                        data["Cate_CID"] = 0
                        data["Cate_FID"] = 0
                        data["flag"] = 0
                        class_result = self.Data_class_filtering(title,class_condition_all)#先使用title进行归类
                        if class_result:
                            data["Cate_CID"] = class_result["Cate_CID"]
                            data["Cate_FID"] = class_result["Cate_FID"]
                        else:#没有匹配到结果进行，词频匹配
                            class_result = self.Data_class_filtering(data["Article_Keyword"], class_condition_all)
                            if  class_result:#有个字段记录没有归类成功
                                data["Cate_CID"] = class_result["Cate_CID"]
                                data["Cate_FID"] = class_result["Cate_FID"]
                        try:
                            self.save_finish_data(data)#将清洗后的数据保存
                            self.update_single_data_clean(id)#更新数据为清洗完成
                        except:
                            a = self.delete_repeat_data(id)
                            print (a)
                    except Exception as e:#插入清洗完成数据库的数据错误表示url或者关键词西游重复
                        print (e)
                self.update_task_finish(_id)#解析任务更改为完成状态
                break
            except Exception as e:
                print (e)
if __name__ == "__main__":
    obj = clean_data()
    task = obj.db_obj.select_clear_task()
    print (task)
    obj.run(task)



