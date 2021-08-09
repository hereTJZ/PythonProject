import threading
import time


# 继承父类threading.Thread，定义带返回值的线程类
class MyThread(threading.Thread):
    # Python的’构造函数‘，自由添加需要的参数
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    # 把要执行的代码写到run函数里面，线程在创建后会直接运行run函数
    def run(self):
        print("启动线程：" + self.name)
        self.result = print_time(self.name, self.delay, 5)
        print("结束线程：" + self.name)

    # 该方法获取线程函数的返回值
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


exitFlag = 0
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
    return threadName


# 创建新线程
t1 = MyThread(1, "Thread-1", 1)
t2 = MyThread(2, "Thread-2", 2)
# 开启线程,执行run方法
t1.start()
t2.start()

t1.join()  # 阻塞主线程，直至t1线程结束，主线程才继续运行
print("线程t1的返回值：" + t1.result)
print("主线程继续运行~")




# 上面通过继承实现多线程，这里直接使用threading库中的线程进行多线程操作
t3 = threading.Thread(target=print_time, args=('Thread-3', 2, 3,))  # 创建线程后需要start()启动，才能执行
t4 = threading.Thread(target=print_time, args=('Thread-4', 1, 3,))

t3.start()
t4.start()

