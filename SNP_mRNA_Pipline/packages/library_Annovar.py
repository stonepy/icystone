Info = """

_ Information ____________________________________________________________________

    Name         : Library_Annovar_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05-0
__________________________________________________________________________________


"""


from packages.process_manager import call_func
from packages.process_manager import multiP_1
from packages.checking        import branchDIR_check
from packages                 import settings
from subprocess               import call
import time



class main:

    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

  ======================================
   Start library with Annovar programme
  ======================================
   [ %s ]\n
        """ % time.ctime()
        print(note_start)


        # _ Parameter preparation ______________________________________________________________________________________

        # Get necessery Info from 'config.ini' and 'settings.py'
        self.OutputDir  = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the OutputDir value
        self.ReportDir  = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the ReportDir value
        self.Species    = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value
        self.Samples    = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list

        # Get parameters from 'setting.py'
        self.Genome     = settings.species_dict[self.Species]['Genome']         # Genome fasta file
        self.AnnovarDir = settings.software_dict["AnnovarDir"]                  #


        # Use for passing parameters to 'process_manager.py'
        self.para_dict = {
            "nProcess" : len(self.Samples),
            "CMDs"     : self.Samples
        }

        # Make sure the directory for annotated '*.vcf' files exists
        self.LibraryDir  = self.OutputDir + "/4_Library"
        branchDIR_check(self.LibraryDir)


        Step0 = \
            """\n_ Library Step 0: Collect GATK results of all samples __________________________________________________________________\n"""

        print("\n%s\n" % Step0)
        with open(self.LibraryDir+"/allSample.step0.vcf", "w") as vcf:
            for sample in self.Samples:
                with open(self.OutputDir+"/3_Calling/%s.vcf" % sample, "r") as gatk:
                    for l in gatk:
                        vcf.write(l)


        Step1 = \
            """\n_ Library Step 1: Annovar, convert GATK results(*.vcf) into Annovar format _____________________________________________\n"""

        CMD_1 = "{AnnovarDir}/convert2annovar.pl --includeinfo -format vcf4 {Input} > {Output} ".format(AnnovarDir=self.AnnovarDir, Input=self.LibraryDir+"/allSample.step1.vcf", Output=self.LibraryDir+"/allSample.step1.annovar")
        print("\n%s\n>>> Executing command:\n%s\n" % (Step1, CMD_1))
        call(CMD_1, shell=True)


        Step2 = \
            """\n_ Library Step 2: Annovar,  _____________________________________________\n"""

        print("\n%s\n" % Step2)
        self.createLib()



    def createLib(self):
        self.LibraryPath = self.LibraryDir + "/allSample.step3.library"



    def callDepthFreq(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir+"/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def annRS(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir+"/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def annoSeq(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir + "/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def annoInDel(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir + "/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def annoBlast(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir + "/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def str_annotation_indel_1(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir + "/<packageName>", sampleName)
        branchDIR_check(DataPreDir)

    def str_annotation_indel_2(self, para_dict, sampleName):
        # Make sure the directory for '*.*' files exists
        DataPreDir = "%s/%s" % (self.OutputDir + "/<packageName>", sampleName)
        branchDIR_check(DataPreDir)


    # Finish Note __________________________________________________________________________________________________
    note_finish = """

=======================================
 Finish library with Annovar programme
=======================================
 [ %s ]\n
        """ % time.ctime()
    print(note_finish)

"""
_ Log _____________________________________________________________________________

2017-05-04
    1) 

___________________________________________________________________________________
"""
