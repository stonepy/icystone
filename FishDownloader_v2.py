"""
- Information --------------------------------------------------------------------
 Name         : FishDownloader
 Description  : Download multiple files simultaneously
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-22
-----------------------------------------------------------------------------------
"""

from multiprocessing import Pool
import time
import urllib
import urllib.request
from subprocess import call

class main:
    def __init__(self):
        pass

    def Download(self, url, path_DL):

        file_name = url.split("/")[-1]

        try:
            print("\nDownload file : %s\nFrom          : %s\n\nDownloading, please ...\n" % (file_name, url))
            # urllib.request.urlretrieve(url, file_name)
            cmd = "wget %s" % url
            call(cmd, shell=True)


        except Exception as e:
            print(e)
            exit()

        print("Finish downloading file : '%s'\n" % file_name)






# ----------------------------------------------------------------
# ----------------------------------------------------------------

class management:
    def __init__(self):
        pass

    def testFunction(self, word):

        def t():
            print(word)
            time.sleep(1)
        t()

    # ------------------------------------------------------------

    """

        Note:

        Apply multiple processes in different ways
            1) no arg
            2) one arg
            3) more than one arg (list)


        Usage:

        This function accepts 2 positional and 1 optional args:
            1) the name of the function
            2) the arg(s)
            3) optional, numbers of processes

    """
    def multiP(self, function_name, args=None, process_num=4):

        start_t = time.time()

        # No argumnet passed
        if args == None :
            p = Pool(process_num)
            for i in range(process_num):
                p.apply_async(function_name)
            p.close()
            p.join()

        # Only one argument passed
        elif isinstance(args, list) == False :
            p = Pool(process_num)
            for i in range(process_num):
                p.apply_async(function_name, args=(args,))
            p.close()
            p.join()

        # Mutiple arguments passed
        elif isinstance(args, list) == True:
            p = Pool(len(args))
            for i in args:
                p.apply_async(function_name, args=(i,))
            p.close()
            p.join()

        total_t = time.time() - start_t
        print("Time concumed: %0.2fs" % total_t)


    def singleP(self):
        pass



if __name__ == "__main__":

    # Parameter Section

    hg = "helloe world"
    words_list = ['default', 'arguments', 'are', 'evaluated', 'once', 'when']
    urls = ['ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna_sm.chromosome.9.fa.gz', "ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna_sm.chromosome.8.fa.gz", "ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna_sm.chromosome.7.fa.gz"]
    process_num = 3


    # Instantiation
    function_name = main().Download

    # Execution part
    management().multiP(function_name, urls, process_num)
