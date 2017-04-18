##########################################################
# Author : Hwx                                           #
# Date   : 2016-10-26                                    #
# Purpose: Select specific OTU and reindex               #
##########################################################


import pandas as pd
import re
import os
import sys


class OTU:

    def __init__(self):

        arg_list  = None
        arg_fasta = None
        arg_out   = None
        args   =[arg_list,arg_fasta,arg_out]

        n = 0
        for arg in sys.argv[1:]:
            args[n] = arg
            n += 1

        usage = "       python otu_filter.py OTU_list OTU_fasta OUTPUT_fasta"
        if args[0] == None or args[1] == None or args[2] == None:
            print
            print 'Usage-Example command:'
            print usage
            print
            exit()

        self.nameInput_OTUlist  = sys.argv[1]
        self.nameInput_OTUfasta = sys.argv[2]
        self.nameOutput         = sys.argv[3]

        self.path_bs = os.getcwd()
        self.output  = os.path.join(self.path_bs, self.nameOutput)

        self.list_ID  = pd.read_csv(os.path.join(self.path_bs, self.nameInput_OTUlist), sep='\t', header=None)
        self.list_ID0 = self.list_ID.ix[:,0]
        self.otu_fa  = pd.read_csv(os.path.join(self.path_bs, self.nameInput_OTUfasta), header=None , sep=';')
        self.otu_fa0 = self.otu_fa[0]


    def select(self):

        seq_tmp = []
        seq = []
        for i in range(len(self.otu_fa[0])):
            if self.otu_fa0[i][0] != '>':
                s = self.otu_fa0[i]
                seq_tmp.append(s)

            if self.otu_fa0[i][0] == '>' or i+1 == len(self.otu_fa[0]):
                seq.append(seq_tmp)
                seq_tmp = []

        del seq[0]


        ID = []
        for id in self.list_ID0:
            ID.append(int(re.findall(r'\d+', id)[0]))

        n = 1
        seq_atr = []
        for id_num in ID:
            seq_atr.append('>OTU' + str(n))
            for se in seq[id_num-1]:
                seq_atr.append(se)
            n += 1

        tmp = pd.Series(seq_atr)
        tmp.to_csv(self.output, index=False, header=False)


otu = OTU()
if __name__ == '__main__':
    otu.select()

