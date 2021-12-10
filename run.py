import time
import threading
import copy

from login_utils import logging
from lecture_utils import print_lecture, set_figure
from multiThread_utils import multi_threads

def main():
    session = logging()     #登录，返回一个会话对象
    print_lecture(session)     #打印讲座信息
    wid = set_figure(session)     #配置抢讲座的信息


    print('已到预约时间，开始抢讲座\n')
    t1 = threading.Thread(target=multi_threads, args=(copy.deepcopy(session), 't1', wid))
    t2 = threading.Thread(target=multi_threads, args=(copy.deepcopy(session), 't2', wid))
    t3 = threading.Thread(target=multi_threads, args=(copy.deepcopy(session), 't3', wid))
    t4 = threading.Thread(target=multi_threads, args=(copy.deepcopy(session), 't4', wid))

    t1.start()
    time.sleep(3)
    t2.start()
    time.sleep(3)
    t3.start()
    time.sleep(3)
    t4.start()
    

if __name__ == '__main__':
    main()