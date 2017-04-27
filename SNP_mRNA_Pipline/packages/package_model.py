Description = """

_ Information ____________________________________________________________________

    Name         : Package Model
    Description  : Model of the package
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_04_24
__________________________________________________________________________________


"""


from packages.process_manager import call_func
from packages.process_manager import multiP_1
from packages.checking        import branchDIR_check
from packages                 import settings
import time



class main:

    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

                              =======================================
                              |                                     |
                              |  Start  with  programme  |
                              |                                     |
                              =======================================


        %s
        """ % time.ctime()
        print(note_start)



        # Finish Note ___________________________________________________________________________________________________
        note_finish = """

                              ========================================
                              |                                      |
                              |  Finish  with  programme  |
                              |                                      |
                              ========================================


        %s
        """ % time.ctime()
        print(note_finish)





"""
_ Log _____________________________________________________________________________


___________________________________________________________________________________
"""
