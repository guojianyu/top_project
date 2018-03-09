
from multiprocessing import Process,Queue
import os,time
class crawl_obj:
    def __init__(self):
        #self.db_obj = DB_Connect.task_opt()#操作数据库对象
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        self.timeout = 30
        self.all_link=[]
        self.tmp_link =[]
    def sacn_add_task(self,myqueue):  # 获取任务的进程，获取的任务添加到队列
        while True:
            try:
                if myqueue.qsize() <= 0:
                    tasks = [[2,3,4,5,6],]# 获取任务
                    if not tasks:
                        time.sleep(1)
                    for task in tasks:  # 填充任务到队列,并将任务更改为就绪状态（1）
                        myqueue.put(task)
                        time.sleep(20)
                        #self.db_obj.update_ctask_status(task[-1])  # 更改任务状态为就绪状态
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
                # 将任务状态更改为执行状态
                print( '获取任务：', task)
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


