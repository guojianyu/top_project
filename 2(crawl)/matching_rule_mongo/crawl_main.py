import os,time
import signal
import DB_Operation
from multiprocessing import Process,Queue
import crawl_task
class crawl_obj:
    def __init__(self):
        self.headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    def sacn_add_task(self,myqueue):  # 获取任务的进程，获取的任务添加到队列
        while True:
            try:
                db_obj = DB_Operation.collection_db()  # 操作数据库对象
                if myqueue.qsize() <= 0:
                    task = db_obj.find_modify({'Task_Status': 0}, {'$set': {'Task_Status': 1,}})  # 获取任务并将任务更改为就绪状态（1）就绪状态
                    if not task:
                        time.sleep(1)
                    else:
                        task = [task['Task_URL'],task['Task_On_rule'],task['Task_Out_rule'],task['Task_Deep'],task['Task_Match_field'],task['Task_Match_rule'],task['Task_isClear'],str(task['_id']),]
                        myqueue.put(task)
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
                #tmp = [task['Task_URL'],task['Task_On_rule'],task['Task_Out_rule'],task['Task_Deep'],task['Task_Match_field'],task['Task_Match_rule'],task['Task_isClear'],task['_id'],]
                pid = os.getpid()
                Task_RID = task[-1]
                Task_PID = pid
                print( '获取任务：',task,'填充pid:', pid)

                """
                # 将任务状态更改为执行状态
                time.sleep(1)
                self.db_obj.update_ctask_status(Task_RID, 2)  # 更改任务状态为2(执行状态)
                self.db_obj.insert_Crawl_Status(Task_RID, Task_PID)# 将执行的任务的一些信息存放到中间数据表，并改变任务状态为可执行状态
                try:
                    if int(task[6]) == 0: # 选择爬取方式
                        # 清理数据
                        #self.clear_url_getdata(task[-1])
                        print('使用requests')
                        crawl_task.crawl_obj().run(task)
                    else:
                        print ('使用无头浏览器：')
                        crawl_task.crawl_obj().selenium_run(task)
                        pass
                    # 执行任务动作
                    self.db_obj.update_ctask_status(Task_RID,4) # 更改任务状态为4(完成状态)
                    self.db_obj.delete_Crawl_Status(Task_RID) # 将中间表中的任务删除
                except Exception as e:
                    self.db_obj.update_ctask_status(Task_RID, 5)  # 更改任务状态为4(完成状态)
                    self.db_obj.delete_Crawl_Status(Task_RID)  # 将中间表中的任务删除
                    print ('执行内部抛出异常:',e)
                """
            except Exception as e:
                print ('执行任务异常：',e)

    def listen_process(self,myqueue):#守护进程
        # 查询数据库，如果在中间表得到暂停字段为暂停则会将该任务关联的进程杀掉，并将运行状态更改为暂停状态。
        # 并删除该条数据，没有暂停数据则休息.
        while True:
            try:
                db_obj = DB_Operation.collection_db()  # 操作数据库对象
                tasks = db_obj.select_stop_Crawl_Status()
                if not tasks:  # 没有任务
                    time.sleep(1)
                    continue
                for task in tasks:
                    Task_RID = task[1]
                    Task_PID = task[2]
                    self.kill(Task_PID)#杀死任务进程，
                    db_obj.delete_Crawl_Status(Task_RID)# 将中间表中的任务删除
                    db_obj.update_ctask_status(Task_RID, 3) # 更改任务状态为3(暂停状态)
                    p = Process(target=self.excutor_task, args=(myqueue,))  # 执行任务的进程
                    p.start()
                    #signal.signal(signal.SIGCHLD,signal.SIG_IGN)
            except Exception as e:
                print ('监听任务出错：',e)

    def run(self):
        tmp_list = []
        #self.db_obj.init_crawl_task() # 初始化任务相关表
        time.sleep(2)
        myqueue = Queue()
        tmp_list.append(Process(target=self.sacn_add_task, args=(myqueue,)))
        for _ in range(6):  # 开启6个进程
            p = Process(target=self.excutor_task, args=(myqueue,)) # 执行任务的进程
            tmp_list.append(p)
        p = Process(target=self.listen_process, args=(myqueue,))# 守护进程负责监控任务
        tmp_list.append(p)
        #signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        for item in tmp_list:
            item.start()
        for item in tmp_list:
            item.join()

if __name__ =='__main__':
    a =  crawl_obj()
    a.run()

