"""
多任务实现方式：
    进程
    线程

多任务：
    定义：
        同一时间内执行多个任务；
    好处：
        多任务的最大好处是充分利用CPU资源，提高程序的执行效率；
    两种表现形式：
        并发：
            定义：
                在一段时间内交替去执行多个任务；
            场景：
                1）任务数量大于CPU的核心数；
        并行：
            定义：
                在一段时间内真正的同时一起执行多个任务；
            场景：
                1）任务数量小于等于CPU的核心数；
进程：
    定义：
        进程(Process) 是资源分配的最小单位，它是操作系统进行资源分配和调度运行的基本单位，通俗理解: 一个正在运行的程
        序就是一个进程.例如:正在运行的qq ,微信等他们都是一个进程。一个程序至少一个进程；
    步骤：
        1.import multiprocessing
        2.进程对象 = multiprocessing.Process()
            参数：
                target：执行的目标任务名，这里指的是函数名(方法名)
                name：进程名，一般不用设置
                group：进程组，目前只能使用None
                args：以元组的方式给执行任务传参
                kwargs：以字典方式给执行任务传参
        3.进程对象.start()
    其他概念：
        进程编号
            作用：
                当程序中进程的数量越来越多时,如果没有办法区分主进程和子进程还有不同的子进程,那么就无法进行有效
                的进程管理,为了方便管理实际上每个进程都是有自己编号的.
            获取方式：
                1.获取当前进程编号:
                    os.getpid()
                2.获取当前父进程编号:
                    os.getppid()
        守护进程：
            设置守护主进程，主进程退出后 子进程直接销毁，不再执行子进程中的代码;
    注意事项：
        1.主进程会等待所有的子进程执行结束再结束；

线程：
    定义：
        进程是分配资源的最小单位, 一旦创建一个进程就会分配一定的资源,就像跟两个人聊QQ就需要打开两个QQ软件
        一样是比较浪费资源的.
        线程是程序执行的最小单位,实际上进程只负责分配资源,而利用这些资源执行程序的是线程,也就说进程是线程的
        少的资源，一但它可与同属一个进程的其它线程共享进程所拥有的全部资源.这就像通过一个QQ软件(一个进程)打开
        两个窗口(两个线程)跟两个人聊天-样,实现多任务的同时也节省了资源.
    特性：
        多线程是Python程序中实现多任务的一种方式；
        线程是程序执行的最小单位；
        同属一个进程的多个线程共享进程所拥有的全部资源；
        线程执行是无序的，由CPU调度决定；
    步骤：
        1.import threading
        2.线程对象 = threading.Thread()
            参数：
                target：执行的目标任务名，这里指的是函数名(方法名)
                name：进程名，一般不用设置
                group：进程组，目前只能使用None
                args：以元组的方式给执行任务传参
                kwargs：以字典方式给执行任务传参
        3.线程对象.start()
进程和线程对比：
    关系对比：
        线程是依附在进程里面的，没有进程就没有线程；
        一个进程默认提供一条线程,进程可以创建多个线程；
    区别对比：
        1.创建进程的资源开销要比创建线程的资源开销要大；
        2.进程是操作系统资源分配的基本单位,线程是CPU调度的基本单位；
        3.线程不能够独立执行，必须依存在进程中；
    优缺点对比：
        1.进程优缺点:
            优点:可以用多核（并行）；
            缺点:资源开销大；
        2.线程优缺点:
            优点:资源开销小；
            缺点:不能使用多核（并发）；
"""
# import os
# import multiprocessing
# import time
#
#
# # 多进程演示---开始
# def sing(num):
#     print('唱歌进程的pid：', os.getpid())
#     print('唱歌父进程的pid：', os.getppid())
#     for i in range(num):
#         print('I am singing ' + str(i))
#         time.sleep(0.5)
#
#
# def dance(num):
#     print('跳舞进程的pid：', os.getpid())
#     print('跳舞父进程的pid：', os.getppid())
#     for i in range(num):
#         print('I am dancing ' + str(i))
#         time.sleep(0.5)
#
#
# # 主进程---开始
# sing_process = multiprocessing.Process(target=sing, args=(5,))  # 子进程
# dance_process = multiprocessing.Process(target=dance, kwargs={'num': 5})  # 子进程
# sing_process.daemon = True  # 设置守护进程
# dance_process.daemon = True
# sing_process.start()
# dance_process.start()
# print('主进程的pid：', os.getpid())
# print('主进程的父进程的pid：', os.getppid())
# time.sleep(1)
# # 主进程---结束
# # 多进程演示---结束


import os
import threading
import time


# 多进程演示---开始
def sing(num):
    for i in range(num):
        print('I am singing ' + str(i))
        time.sleep(0.5)


def dance(num):
    for i in range(num):
        print('I am dancing ' + str(i))
        time.sleep(0.5)


# 主进程---开始
sing_thread = threading.Thread(target=sing, args=(5,))  # 子进程
dance_thread = threading.Thread(target=dance, kwargs={'num': 5})  # 子进程
sing_thread.daemon = True  # 设置守护主线程，也可以在生成对象的时候传入daemon参数
dance_thread.setDaemon(True)
sing_thread.start()
dance_thread.start()
time.sleep(1)
# 主进程---结束
# 多进程演示---结束