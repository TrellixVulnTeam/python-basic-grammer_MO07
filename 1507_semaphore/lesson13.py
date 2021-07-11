"""
セマフォはロック中に動作できるスレッド数を指定できる
"""
import logging
import threading
import time


logging.basicConfig(
    level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(semaphore):
    with semaphore:               # semaphore取得することで、他スレッドはこのスレッドがreleaseされるまで実行されない
        logging.debug('start')
        time.sleep(5)        # これをすると、worker1,2もx=1
        logging.debug('end')
def worker2(semaphore):
    with semaphore:               # semaphore取得することで、他スレッドはこのスレッドがreleaseされるまで実行されない
        logging.debug('start')
        time.sleep(5)        # これをすると、worker1,2もx=1
        logging.debug('end')
def worker3(semaphore):
    with semaphore:               # semaphore取得することで、他スレッドはこのスレッドがreleaseされるまで実行されない
        logging.debug('start')
        time.sleep(5)        # これをすると、worker1,2もx=1
        logging.debug('end')



if __name__ == '__main__':
    d = {'x': 0}
    semaphore = threading.Semaphore(2)    # 2つのスレッドがロックをかけられる
    t1 = threading.Thread(target=worker1, args=(semaphore,))
    t2 = threading.Thread(target=worker2, args=(semaphore,))
    t3 = threading.Thread(target=worker3, args=(semaphore,))
    t1.start()
    t2.start()
    t3.start()
