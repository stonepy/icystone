
# # Convert mouse GTF chromesome "M" to "MT"
# import re
#
#
# with open("gencode.nochr.gtf", "r") as gtf:
#
#     output = open("gencode.nochr.hwx.gtf", "w")
#     for l in gtf:
#         if l.startswith("M"):
#             origin  = "M"
#             replace = "MT"
#             l = re.sub(origin, replace, l, count=1)
#         output.write(l)
#
#     output.close()
#
#

# from concurrent.futures import ThreadPoolExecutor
#
# import shutil
# import time
#
# def worker1():
#     time.sleep(1)
# def worker2():
#     time.sleep(2)
# def worker3():
#     time.sleep(3)
#
# with ThreadPoolExecutor(max_workers=4) as e:
#     e.submit(worker1)
#     e.submit(worker2)
#     e.submit(worker3)
#
#
#
#
#
# import multiprocessing
# from multiprocessing import Pool
# import time
# import sys
#
#
# def worker(t):
#     print("wait %s ..." % str(t))
#     time.sleep(t)
#
# def ctrlC(p):
#     while 1 != 0:
#         try:
#             pass
#         except KeyboardInterrupt:
#             p.terminate()
#
# p = Pool(4)
# for i in range(3):
#     p.apply_async(worker, args=(i, ))
#     print()
# p.apply_async(ctrlC, args=(p, ))
# p.close()
# p.join()



# import signal
# import sys
# def signal_handler(signal, frame):
#         print('You pressed Ctrl+C!')
#         sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C')
# signal.pause()
#
#
# import multiprocessing
# from multiprocessing import Pool
# import time
# import signal
#
#
# def worker():
#     while True:
#         print(time.time())
#         time.sleep(.5)
#
# def worker_init():
#     # ignore the SIGINI in sub process, just print a log
#     def sig_int(signal_num, frame):
#         print('signal: %s' % signal_num)
#     signal.signal(signal.SIGINT, sig_int)
#
#
# pool = Pool(2, worker_init)
# result = pool.apply_async(worker)
# while True:
#     try:
#         result.get(0xfff)
#     # catch TimeoutError and get again
#     except multiprocessing.TimeoutError as ex:
#         print('timeout')
