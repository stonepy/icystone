import multiprocessing
from multiprocessing import Pool
import time
import signal


def worker():
    while True:
        print(time.time())
        time.sleep(.5)

def worker_init():
    # ignore the SIGINI in sub process, just print a log
    def sig_int(signal_num, frame):
        print('signal: %s' % signal_num)
    signal.signal(signal.SIGINT, sig_int)


pool = Pool(2, worker_init)
result = pool.apply_async(worker)
while True:
    try:
        result.get(0xfff)
    # catch TimeoutError and get again
    except multiprocessing.TimeoutError as ex:
        print('timeout')


import multiprocessing
from multiprocessing import Pool
import time


def worker(t):
    print("wait %s ..." % str(t))
    time.sleep(t)

def ctrlC():
    while 1 != 0:
        try:
            pass
        except KeyboardInterrupt:
            exit()

p = Pool(4)
for i in range(3):
    p.apply_async(worker, args=(i, ))
p.apply_async(ctrlC)
p.close()
p.join()