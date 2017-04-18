###########################################################
# Author  : Hwx                                           #
# Date    : 2016-10-27                                    #
# Purpose : Use for select particular sequences in fasta  #
# Version : v1                                            #
###########################################################


import sys


class fil_fa:

    def __init__(self):

    # Collect parameters from inpput
        arg_name   = None
        arg_fasta  = None
        arg_outTar = None
        arg_outRes = None
        args   =[arg_name,arg_fasta,arg_outTar,arg_outRes]

        n = 0
        for arg in sys.argv[1:]:
            args[n] = arg
            n += 1

    # Usage
        usage = "       python 'script_path'/filter_fasta_v1.py ../Name_Of_Target ../Input.fasta ../Output_Target_Name.fasta ../Output_other_Name.fasta"
        if args[0] == None or args[1] == None or args[2] == None or args[3] == None:
            print
            print 'Usage-Example Command:'
            print usage
            print
            exit()

    # Source and filter name
        self.name_filter = args[0]
        self.fasta       = args[1]
        self.output_tar  = args[2]
        self.output_res  = args[3]

# Selector
    def filter_fasta(self):

    # Beging to work with opening the ***.fasta file
        with open(self.fasta, "r") as fa:

        # Seperate the seqs by the name given
            # Set of output seqs
            tar_fa = []
            res_fa = []

            for l in fa:
            # Acquire the particular title
                if l.startswith('>' + self.name_filter):
                    tar_fa.append(l)
                    target = 'on'

            # Collect the particular seqs
                elif not l.startswith('>') and target == 'on':
                    tar_fa.append(l)

            # Acquire the rest title
                elif l.startswith('>') and l.find('hsa') == -1:
                    res_fa.append(l)
                    target = 'off'

            # Collect the rest seqs
                elif not l.startswith('>') and target == 'off':
                    res_fa.append(l)

        # Output seperated seqs

            # Target seqs
            with open(self.output_tar, 'w') as tarfa:
                for lr in tar_fa:
                    ld = lr.replace('U','T')
                    tarfa.write(ld)

            # Rest of the seqs
            with open(self.output_res, 'w') as resfa:
                for lr in res_fa:
                    ld = lr.replace('U', 'T')
                    resfa.write(ld)



fil_fa = fil_fa()
if __name__ == '__main__':
    fil_fa.filter_fasta()
