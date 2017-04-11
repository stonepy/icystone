###########################################################
# Author  : Hwx                                           #
# Date    : 2016-12-22                                    #
# Name    : Chromosome_size                               #
# Version : v1                                            #
# Description : Chromosome size conunting                 #
###########################################################



import time
with open("TAIR10_chr_all.fa") as fa:
    chr  = []
    seq  = ""
    size = []

    for l in fa:
        if l.startswith(">C"):
            chr.append(l.split(" ")[0][1:-1])
            if seq != "":
                size.append(len(seq))
                seq = ""
        else:
            seq += l
    size.append(len(seq))
    print chr
    print size

    with open("Chromsome_size.txt", "w+") as cs:
        for i in range(len(chr)):
            cs.write(chr[i] + " " + str(size[i]) + "\n")
