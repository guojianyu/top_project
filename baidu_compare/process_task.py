import DB_Operation
from multiprocessing import Process,Queue
import os,time
import new_compare_baidu
obj = DB_Operation.collection_db()
class crawl_obj:
    def __init__(self):
        #self.db_obj = DB_Connect.task_opt()#操作数据库对象
        pass
    def sacn_add_task(self,myqueue):  # 获取任务的进程，获取的任务添加到队列
        while True:
            try:
                if myqueue.qsize() <= 0:
                    tasks = obj.select_task_id()# 获取任务
                    if not tasks:
                        time.sleep(1)
                    for task in tasks:  # 填充任务到队列,并将任务更改为就绪状态（1）
                        myqueue.put(task)
                    #print('任务队列长度：', myqueue.qsize())
            except Exception as e:
                print ('填充任务列表出错：',e)
    def kill(self,pid):#杀死进程
        try:
            a = os.kill(int(pid), 9)
            print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
        except OSError as e:
            print('没有此进程!!!')

    def excutor_task(self,myqueue):  # 执行任务
        while True:
            try:
                task = myqueue.get()
                print('获取任务：', task,type(task))
                # 将任务状态更改为执行状态
                try:
                    #new_compare_baidu.Baidu_compare().run(task)
                    pass
                except:
                    pass

                # 执行任务动作
            except Exception as e:
                print ('执行任务异常：',e)

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


if __name__ =='__main__':
    a =  crawl_obj()
    a.run()


