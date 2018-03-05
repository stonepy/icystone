test_http = "https://download.jetbrains.com/python/pycharm-community-2017.3.3.tar.gz"


""" USER SETTING """
download_addresses = [
    "https://download.jetbrains.com/python/pycharm-community-2017.3.3.tar.gz",
    "",
]
user_setting = dict(
    download_simultaneously = 2,
)

""""""""""""""""""""


import os
import sys
import time
import subprocess as subp
import multiprocessing as mulp



""" Other Tools """
def timer(func):
    """ It's a Timer, decorator """
    def total_time(*args):
        Ts = time.time()
        res = func(*args)
        Tf = time.time()
        Tt = Tf - Ts

        minute, seconds = divmod(Tt, 60)
        hours, minutes  = divmod(minute, 60)
        print("Comsumed time: %02d:%02d:%02d \n" % (hours, minute, seconds))

        return res
    return total_time


def address_prepare(download_addresses):
    address_list = []
    for i in download_addresses:
        if len(i) != 0:
            address_list.append(i)
    address_list = list(set(address_list))
    return address_list


def downloader(address):
    cmd = "wget -c %s\n" % address
    subp.call(cmd, shell=True)
    print(cmd)


@timer
def main():
    nProcess = user_setting["download_simultaneously"]
    address_list = address_prepare(download_addresses)
    p = mulp.Pool(nProcess)
    for addr in address_list:
        p.apply_async(downloader, args=[addr, ])
    p.close()
    p.join()



if __name__ == "__main__":
    main()
