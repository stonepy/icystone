Info = """

_ Information ____________________________________________________________________

    Name         : Main__Whole_Transcriptome_Sequencing_Pipline
    Description  : For Whole_Transcriptome_Sequencing analysis
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05_
__________________________________________________________________________________
"""



import sys
import os
import time

from os.path import join as pjoin
from Packages import main



""" _ 3. Execution Control _________________________________________________________________________________________ """
if __name__ == "__main__":
    t_start = time.time()       # Start time
    prep = main.preparation()
    print(prep.note_start)      # Start note



# ======================================================================================================================

    # _ 1) Preparation _________________________________________________________________________________________________
    # Comment this line to skip whole preparation then test the Pipline manually
    prep.get_args()
    WTS_cfg_dict = prep.config()
    # prep.check()

    # _ 2) Workflow ____________________________________________________________________________________________________
    print(prep.note_running)        # Running note
    workflow = main.workflow(WTS_cfg_dict)     # Comment this line to shut whole Pipline function down and test the workflow
    # workflow.qc()

# ======================================================================================================================



    print(prep.note_finish)  # Finish note
    print("\n\n>>> Run time: [ %.2fs: %im: %ih: %id ] (Total second(s): %.2fs)\n" % (prep.timer(t_start)))

""" _ END __________________________________________________________________________________________________________ """



# _ ALl modules needed ________________
modules_dict = """

_ need to be developed ________________

"""


"""
_ Log ___________________________________________________________________________

2017-05-12
    1) Start Today
    2) Revised from 'SNP_mRNA_Pipline.py'
    3) Seperate this script into two, another name 'main.py', move all fucntions
        to 'main.py', left basic lines here for easier management

_________________________________________________________________________________
"""
