import DB_Operation
import main
from multiprocessing import Process,Queue
import os,time
import threading

db_obj = DB_Operation.collection_db()
class crawl_obj:
    def __init__(self):
        pass

    def sacn_add_task(self,myqueue):  # 获取任务的进程，获取的任务添加到队列
        while True:
            try:
                if myqueue.qsize() <= 0:
                    clear_task = db_obj.select_clear_task()
                    if clear_task:
                        myqueue.put( clear_task)
            except Exception as e:
                print (e)

    def kill(self,pid):#杀死进程
        try:
            a = os.kill(int(pid), 9)
            print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
        except OSError as e:
            print('没有此进程!!!')

    def excutor_task(self,myqueue):  # 执行任务
        thread_all = []
        for _ in range(10):
            t = threading.Thread(target= main.clean_data().run())
            t.start()
            thread_all.append(t)
        for thr in thread_all:
            thr.join()

    def run(self):
        tmp_list = []
        myqueue = Queue()
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


