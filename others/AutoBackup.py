"""
    Backup/Restore with Server2#:
        Backup to Server2#
        Restore from Server2#
        Adapt to Linux/MacOS system (My work PC and MacBook)
"""



import argparse
import subprocess as sb
import platform as pl

__Description__ = ""



# _ Arguments __________________________________________________________________________

def get_args():

    import argparse
    parser = argparse.ArgumentParser(description=__Description__)

    #
    # parser.add_argument("Input_BAM_PATH", help="")
    parser.add_argument("-R", "--Restore", help="Restore the directories", action='store_true')
    parser.add_argument("-B", "--Backup", help="Backup the directories", action='store_true')

    args = parser.parse_args()

    return args

# _ Arguments __________________________________________________________________ End ___





local_dir = {

    "TumorSNV_B_Linux"  :   "/media/daniel/Data/ExonTumor_Project",
    "TumorSNV_R_Linux"  :   "/media/daniel/Data/.",
    "TumorSNV_B_MacOS"  :   "/Users/IcyMount/Desktop/ExonTumor_Project",
    "TumorSNV_R_MacOS"  :   "/Users/IcyMount/Desktop/.",
    ""  :   "",
    ""  :   "",

}


server2_dir = {

    "TumorSNV_B_Server"  :   "/home/hwx/DevPipline/Tumor_SNP_Hwx/.",
    "TumorSNV_R_Server"  :   "/home/hwx/DevPipline/Tumor_SNP_Hwx/ExonTumor_Project",
    ""  :   "",

}




args = get_args()

if args.Backup == True:

    if "Linux" in pl.system():
        Bcmd = "scp -r %s hwx@192.168.0.2:%s" % (local_dir["TumorSNV_B_Linux"], server2_dir["TumorSNV_B_Server"])
    elif "Darwin" in pl.system():
        Bcmd = "scp -r %s hwx@192.168.0.2:%s" % (local_dir["TumorSNV_B_MacOS"], server2_dir["TumorSNV_B_Server"])

    sb.call(Bcmd, shell=True)
    exit()


if args.Restore == True:

    if "Linux" in pl.system():
        Rcmd = "scp -r hwx@192.168.0.2:%s %s" % (server2_dir["TumorSNV_R_Server"], local_dir["TumorSNV_R_Linux"])
    elif "Darwin" in pl.system():
        Rcmd = "scp -r hwx@192.168.0.2:%s %s" % (server2_dir["TumorSNV_R_Server"], local_dir["TumorSNV_R_MacOS"])

    sb.call(Rcmd, shell=True)
    exit()


