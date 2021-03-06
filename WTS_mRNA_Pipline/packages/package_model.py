Info = """

_ Information ____________________________________________________________________

    Name         : Package Model
    Description  : Model of the package
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05-02
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
   Start  with  programme
  =======================================
    %s\n
        """ % time.ctime()
        print(note_start)


        # _ Parameter preparation ______________________________________________________________________________________

        # Get necessery Info from 'config.ini' and 'settings.py'
        self.OutputDir  = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the OutputDir value
        self.ReportDir  = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the ReportDir value
        self.Species    = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value
        self.bed        = config_dict["section_3"]["2_"].split(" ")[-1]     # Split out the bed value
        self.Samples    = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list

        # Get parameters from 'setting.py'
        self.Genome     = settings.species_dict[self.Species]['Genome']         # Genome fasta file
        self.Tmp        = settings.software_dict["Tmp"]          #
        self.JAVA       = settings.software_dict["JAVA"]         #
        self.PicardDir  = settings.software_dict["PicardDir"]    #
        self.GATK       = settings.software_dict["GATK"]         #
        self.Samtools   = settings.software_dict["Samtools"]     #
        self.Threshold  = settings.software_dict["PreGATK"]      #


        # Use for passing parameters to 'process_manager.py'
        self.para_dict = {
            "nProcess" : len(self.Samples),
            "CMDs"     : self.Samples
        }

        # Assign tasks
        multiP_1(self.para_dict, self.run)


    def run(self, para_dict, sampleName):

        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir+"/<packageName>", sampleName)
        branchDIR_check(DataPreDir)


        # Finish Note __________________________________________________________________________________________________
        note_finish = """

  =======================================
   Finish  with  programme
  =======================================
    %s\n
        """ % time.ctime()
        print(note_finish)





"""
_ Log _____________________________________________________________________________


___________________________________________________________________________________
"""
