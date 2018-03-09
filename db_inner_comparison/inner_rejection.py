#对文章数据库内部剔重
import time
import jieba_cut
import DB_Connect
from multiprocessing import Process,Queue
"""
先按自增id 排序，每次取若干条，对比文章达到临界值的就删除。比对结束一组就记录最后一个自增ID再取一组，
直到对比结束，结束后将文章的内部剔重标识写入1。
同时多个进程进行此项运算。
"""
class rejection:
    def __init__(self,max_similar=1):
        self.db_obj = DB_Connect.task_opt()  # 操作数据库对象
        self.max_similar = max_similar#用户设置的最大相似度，达到该值就将对应的文章进行记录
        pass
    def sacn_add_task(self, myqueue):  # 获取任务的进程，获取的任务添加到队列
        while True:
            try:
                last_id = self.db_obj.get_Maxrid_Article_List()
                task = self.db_obj.select_article_task(last_id)#获取任务
                print('获取任务：', task)
                if not task:
                    time.sleep(1)
                    continue
                task = task[0]#提取一个任务
                max_id = task[0]#提取ID
                print ('max_id:',max_id)
                while True:
                    tmp = [task[0],]
                    if myqueue.qsize() >= 6:
                        time.sleep(1)
                        continue
                    res = self.db_obj.select_Article_List(max_id)
                    if not res:
                        print(max_id,'结束')
                        break
                    max_id = res[-1][0]#得到最大的id
                    min_id = res[0][0]#最大ID
                    tmp.append(min_id)
                    tmp.append(max_id)
                    myqueue.put(tmp)# 将比对文章和要比对的文章填充到列表[(),[(),()]]
                    self.db_obj.update_Article_maxid(task[0], max_id)# 将入队列的最大自增ID记录
            except Exception as e:
                print (e)

    def filter_article(self,art_id,compare_min_id,compare_max_id):
        article_res = self.db_obj.select_article_content(art_id)#得到需要比较的源文章
        article_coll = self.db_obj.select_article_center_content(compare_min_id,compare_max_id)#取出文章集合
        for art in  article_coll:#将比较文章与其他文章进行对比，如果大于某个相似度则将该文章的删除状态更改为删除状态
            similar = jieba_cut.similarity(article_res[0], art[1])
            if similar >= self.max_similar:#相似度达到预设值进行记录
                self.db_obj.update_Article_delete(art[0],1)#改为删除状态
        #比对结束，然后将最后一个文章的RID记录
        return 0

    def excutor_task(self,myqueue):#执行任务
        while True:
            try:
                result = myqueue.get()
                print ('得到任务：',result)
                art_id = result[0]#比对文章
                compare_min_id = result[1]#比的最小文章RID
                compare_max_id = result[2]#比较的最大rid
                start = time.time()
                max_id = self.filter_article(art_id,compare_min_id,compare_max_id)#返回最大ID
                print ('比较结束一组数据中的最大id是:',max_id)
                print('比较完该组数据用时：',time.time()-start,'s')
                #查找大于自身id的文章，进行比较
                # 执行任务动作
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

if __name__ == '__main__':
    obj = rejection(max_similar=0.96)
    obj.run()