import time
from multiprocessing import Pool

global para_dict
para_dict = {
    "nProcess": 2,
    "CMDs": ["hello", "world"]
}

def multiP_1(para_dict, func):

    start_t = time.time()
    P = Pool(para_dict["nProcess"])

    for i in para_dict["CMDs"]:
        res = P.apply_async(func, args=(i,))
        # print(res)
    # P.apply_async(ctrlC)        # Temporary for testing, 2017-04-25
    P.close()
    P.join()
    total_t = time.time() - start_t
    print("Time consumed: %0.2fs" % total_t)

class a:

    def __init__(self):

        # multiP_1(para_dict, a().test)
        print("sdfdsdsdsf")

    def test(self, word):
        print(word)




multiP_1(para_dict, a().test)





