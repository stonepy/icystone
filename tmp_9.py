"""
Trash recycling

"""


import os
import sys
import shutil


opt_default = {

    "backup_dir"   :   "",
    "restore_dir"  :   "",
    "backup_file"  :   os.listdir(),

}


opt_1 = {

    "backup_dir"   :   "",
    "restore_dir"  :   "",
    "backup_file"  :   [],

}


def backup






if __name__ == "__main__":

    try:
        opt = sys.args[1]
        if opt == "1":
            opt_setting = opt_default

    except:
        opt = opt_default
        opt_setting["backup_dir"]  = "./tmp"
        opt_setting["restore_dir"] = "."

        try:
            os.makedirs(opt_setting["backup_dir"])
        except:
            pass


    try:
        bs_opt = sys.args[2]

    except:
