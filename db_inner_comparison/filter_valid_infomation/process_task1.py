#扫描数据库，提取有用数据
import time
import jieba.analyse
import xlrd
import DB_Connect
from multiprocessing import Process,Queue

class filter:
    def __init__(self):
        self.db_obj = DB_Connect.task_opt()#操作数据库对象
        workbook = xlrd.open_workbook(r'匹配词.xlsx')
        sheet1 = workbook.sheet_by_name('Sheet1')
        self.col_content = sheet1.col_values(0)

    def sacn_add_task(self, myqueue): # 获取任务的进程，获取的任务添加到队列
        max_rid = 20000000
        while True:
            try:
                if myqueue.qsize() <= 0:
                    data_list= self.db_obj.look1(max_rid)
                    if data_list:
                        myqueue.put(data_list)
                        max_rid = data_list[-1][0]
                    else:
                        time.sleep(1)
            except Exception as e:
                print (e)

    def cut_word(self,article):
        # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
        res = jieba.analyse.extract_tags(
            sentence=article, allowPOS=('n', '1', 'ns', 'v'))
        return res

    def filter_valid_info(self,data_list):#过滤有效信息
        for item in data_list:
            #print('标题:', item[1])
            self.record_word_excel(item[1],item[0])
        pass

    def record_word_excel(self,title,rid):
        find_flag = 0
        for word in self.col_content:
            if word in title:
                find_flag = 1
                break
        if not find_flag:
            self.db_obj.match_lost(rid)
            #print('没有匹配到的标题为：',title)
        else:
            self.db_obj.match_sucess(rid,word)
            #print('匹配到的标题：',rid,title)

    def excutor_task(self,myqueue):#执行任务
        while True:
            try:
                result = myqueue.get()
                print ('得到任务：')
                self.filter_valid_info(result)
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
    #data_list = obj.db_obj.look1(0)
    #obj.filter_valid_info(data_list)
    obj.run()
    print (obj.col_content)