Info = """

_ Information ____________________________________________________________________

    Name         : dataPre_Picard_GATK_SNP_mRNA
    Description  : Prepare data for seeking INDEL/SNP with GATK programme
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05_02
__________________________________________________________________________________


"""


from packages.checking        import branchDIR_check
# from packages.checking        import finish_check
from packages.process_manager import multiP_1
from packages                 import settings
from subprocess               import call
import time
import os


class main:

    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |                                                      |
  |  Start BAM preparation with Picard & GATK programme  |
  |                                                      |
  ========================================================

  %s\n
        """ % time.ctime()
        print(note_start)


        # _ Parameter preparation _____________________________________________________________________________________

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
        self.Threshold  = settings.software_dict["PreGATK"]      # No use in this module


        # Use for passing parameters to 'process_manager.py'
        self.para_dict = {
            "nProcess" : len(self.Samples),
            "CMDs"     : self.Samples
        }

        # Assign preparation tasks
        multiP_1(self.para_dict, self.run)



        # Finish Note __________________________________________________________________________________________________
        note_finish = """

  =========================================================
  |                                                       |
  |  Finish BAM preparation with Picard & GATK programme  |
  |                                                       |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  %s\n
        """ % time.ctime()
        print(note_finish)


    """ _ BAM preparation __________________________________________________________________________________________ """
    def run(self, sampleName):

        # If "dbSNP" and "InDel" exist, only human and mouse for the temporary. For Step6, Step7.
        # knownDBsnp, knownSiteDBsnp, knownInDel = "", "", ""
        if "dbSNP" in settings.species_dict[self.Species]:
            knownDBsnp     = "-known " + settings.species_dict[self.Species]["dbSNP"]
            knownSiteDBsnp = "-knownSites " + settings.species_dict[self.Species]["dbSNP"]

        if "InDel" in settings.species_dict[self.Species]:
            knownInDel     = "-known " + settings.species_dict[self.Species]["InDel"]

        # Make sure the directory for '*.bam' files exists
        DataPreDir = "%s/%s" % (self.OutputDir+"/2_DataPre", sampleName)
        branchDIR_check(DataPreDir)     # Directory check


        Step1 = \
            """\n_ DataPre Step 1 Picard. BAM, convert '*.sam' with the '*.bam' file, results of STAR mapping __________________________\n"""

        sam_path = "%s/%s/%s.step2.Aligned.out.sam" % (self.OutputDir+"/1_Mapping", sampleName, sampleName)        # Input '*.sam' data
        bam_path = "%s/%s.bam" % (DataPreDir, sampleName)
        CMD_1 = "more {sam} | {Samtools} view -bS -L {bed} -h -F 4 - > {bam}".format(sam=sam_path, Samtools=self.Samtools, bed=self.bed, bam=bam_path)
        print("\n%s\n>>> Executing command:\n%s" % (Step1, CMD_1))
        call(CMD_1, shell=True)


        Step2 = \
            """\n_ DataPre Step 2 Picard. Sort, '*.bam' file sorting ___________________________________________________________________\n"""

        bamSort_path      = "%s/%s_sort.bam" % (DataPreDir, sampleName)
        bamSortIndex_path = "%s/%s_sort.bai" % (DataPreDir, sampleName)
        CMD_2_1 = "{JAVA} -jar -Xmx6g {PicardDir}/SortSam.jar INPUT={bam} OUTPUT={bam_sort} SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam=bam_path, bam_sort=bamSort_path, Tmp=self.Tmp)
        CMD_2_2 = "{JAVA} -jar -Xmx6g {PicardDir}/BuildBamIndex.jar INPUT={bam_sort} OUTPUT={bam_sort_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_sort_idx=bamSortIndex_path, Tmp=self.Tmp)
        print("\n%s\n>>> Executing command:\n%s" % (Step2, CMD_2_1))
        print("\n>>> Executing command:\n%s\n" % CMD_2_2)
        call(CMD_2_1, shell=True)
        call(CMD_2_2, shell=True)


        Step3 = \
            """\n_ DataPre Step 3 Picard. Mark Duplicates, mark duplicates in the '*.bam' file _________________________________________\n"""

        bamDup_path        = "%s/%s_sort_dup.bam" % (DataPreDir, sampleName)
        bamDupMetrics_path = "%s/%s_dup.metrics" % (DataPreDir, sampleName)     # Copy '*_dup.metrics' to 'Report' dir, but I haven't do it
        bamDupIndex_path   = "%s/%s_sort_dup.bai" % (DataPreDir, sampleName)
        CMD_3_1 = "{JAVA} -jar -Xmx8g {PicardDir}/MarkDuplicates.jar INPUT={bam_sort} OUTPUT={bam_dup} METRICS_FILE={bam_dup_metrics} REMOVE_DUPLICATES=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_dup=bamDup_path, bam_dup_metrics=bamDupMetrics_path, Tmp=self.Tmp)
        CMD_3_2 = "{JAVA} -jar -Xmx8g {PicardDir}/BuildBamIndex.jar INPUT={bam_dup} OUTPUT={bam_dup_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_dup=bamDup_path, bam_dup_idx=bamDupIndex_path, Tmp=self.Tmp)
        print("\n%s\n>>> Executing command:\n%s" % (Step3, CMD_3_1))
        print("\n>>> Executing command:\n%s\n" % CMD_3_2)
        call(CMD_3_1, shell=True)
        call(CMD_3_2, shell=True)


        Step4 = \
            """\n_ DataPre Step 4 Picard. Add Reads Group, add reads group to the '*.bam' file _________________________________________\n"""

        bamGroup_path      = "%s/%s_sort_dup_group.bam" % (DataPreDir, sampleName)
        bamGroupIndex_path = "%s/%s_sort_dup_group.bai" % (DataPreDir, sampleName)
        CMD_4_1 = "{JAVA} -jar -Xmx16g {PicardDir}/AddOrReplaceReadGroups.jar I={bam_dup} O={bam_group} SO=coordinate ID={sample} LB={sample} PL=illumina PU=barcode SM={sample} CREATE_INDEX=false VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_dup=bamDup_path, bam_group=bamGroup_path, sample=sampleName, Tmp=self.Tmp)
        CMD_4_2 = "{JAVA} -jar -Xmx8g {PicardDir}/BuildBamIndex.jar INPUT={bam_group} OUTPUT={bam_group_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_group=bamGroup_path, bam_group_idx=bamGroupIndex_path, Tmp=self.Tmp)
        print("\n%s\n>>> Executing command:\n%s" % (Step4, CMD_4_1))
        print("\n>>> Executing command:\n%s\n" % CMD_4_2)
        call(CMD_4_1, shell=True)
        call(CMD_4_2, shell=True)


        Step5 = \
            """\n_ DataPre Step 5 GATK/Picard. Split 'N' Trim, Split 'N' and trim from the '*.bam' file ________________________________\n"""

        bamTrim_path      = "%s/%s_sort_dup_group_trim.bam" % (DataPreDir, sampleName)
        bamTrimIndex_path = "%s/%s_sort_dup_group_trim.bai" % (DataPreDir, sampleName)
        CMD_5_1 = "{JAVA} -jar {GATK} -T SplitNCigarReads -R {Genome} -I {bam_group} -o {bam_trim} -U ALLOW_N_CIGAR_READS -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_group=bamGroup_path, bam_trim=bamTrim_path)
        CMD_5_2 = "{JAVA} -jar -Xmx8g {PicardDir}/BuildBamIndex.jar INPUT={bam_trim} OUTPUT={bam_trim_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_trim=bamTrim_path, bam_trim_idx=bamTrimIndex_path, Tmp=self.Tmp)
        print("\n%s\n>>> Executing command:\n%s" % (Step5, CMD_5_1))
        print("\n>>> Executing command:\n%s\n" % CMD_5_2)
        call(CMD_5_1, shell=True)
        call(CMD_5_2, shell=True)


# **********************************************************************************************************************
# >>>Question: It's so strange that why Step 6 use 'knownDBsnp' as same as Step 7, but there is no check in Step 6 while there it is in Step 7
# <<<Answer: Because if Step 6 can run without this parameter, it will be empty if there is no 'knownDBsnp' exist, refer to the parameter preparation

        Step6 = \
            """\n_ DataPre Step 6 GATK. Realignment, realign around the INDLEs _________________________________________________________\n"""

        bamRealign_path          = "%s/%s_sort_dup_group_trim_realign.bam" % (DataPreDir, sampleName)
        bamRealignIntervals_path = "%s/%s_sort_dup_group_trim_realign.intervals" % (DataPreDir, sampleName)
        CMD_6_1 = "{JAVA} -jar {GATK} -l INFO -T RealignerTargetCreator -R {Genome} -I {bam_trim} -o {bam_realign_intervals} {knownDBsnp} {knownInDel} --validation_strictness LENIENT".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_trim=bamTrim_path, bam_realign_intervals=bamRealignIntervals_path, knownDBsnp=knownDBsnp, knownInDel=knownInDel)
        CMD_6_2 = "{JAVA} -jar {GATK} -l INFO -T IndelRealigner -R {Genome} -I {bam_trim} -o {bam_realign} {knownInDel} -targetIntervals {bam_realign_intervals} --validation_strictness LENIENT".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_trim=bamTrim_path, bam_realign=bamRealign_path, knownInDel=knownInDel, bam_realign_intervals=bamRealignIntervals_path)
        print("\n%s\n>>> Executing command:\n%s" % (Step6, CMD_6_1))
        print("\n>>> Executing command:\n%s\n" % CMD_6_2)
        call(CMD_6_1, shell=True)
        call(CMD_6_2, shell=True)


        Step7 = \
            """\n_ DataPre Step 7 GATK. Base Quality Score Recalibration. Caution: this Step works only when 'dbSNP' exists ____________\n"""

        bamRecalibrator_path      = "%s/%s_sort_dup_group_trim_realign_recalibrator.bam" % (DataPreDir, sampleName)
        bamRecalibratorIndex_path = "%s/%s_sort_dup_group_trim_realign_recalibrator.bai" % (DataPreDir, sampleName)     # No use
        recal_path                = "%s/%s_recal.table" % (DataPreDir, sampleName)
        CMD_7_1 = "{JAVA} -jar {GATK} -l INFO -T BaseRecalibrator -R {Genome} {knownSitesDBsnp} -I {bam_realign} --validation_strictness LENIENT -o {recal}".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, knownSitesDBsnp=knownSiteDBsnp, bam_realign=bamRealign_path, recal=recal_path)
        CMD_7_2 = "{JAVA} -jar {GATK} -l INFO -T PrintReads -R {Genome} -BQSR {recal} --validation_strictness LENIENT -I {bam_realign} -o {bam_recalibrator}".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, recal=recal_path, bam_realign=bamRealign_path, bam_recalibrator=bamRecalibrator_path)

        # Skip this Step when there is no 'dbSNP'
        if os.path.exists(knownSiteDBsnp.split(" ")[-1]):

            print("\n%s\n>>> Executing command:\n%s" % (Step7, CMD_7_1))
            print("\n>>> Executing command:\n%s\n" % CMD_7_2)
            call(CMD_7_1, shell=True)
            call(CMD_7_2, shell=True)

            FinalInputBam_path = bamRecalibrator_path       # For Step 8

        else:
            print("\n>>> Warning: 'dbSNP' (of '%s'), database of known SNPs, is not available, thus skip Base Quality Score Recalibration\n" % self.Species)
            FinalInputBam_path = bamRealign_path

# **********************************************************************************************************************


        Step8 = \
            """\n_ DataPre Step 8 Picard. Final, output the finally processed '*.bam' file _____________________________________________\n"""

        bamFinal_path      = "%s/%s_final.bam" % (DataPreDir, sampleName)
        bamFinalIndex_path = "%s/%s_final.bai" % (DataPreDir, sampleName)
        CMD_8_1 = "{JAVA} -jar {PicardDir}/SortSam.jar INPUT={FinalInputBam} OUTPUT={bam_final} SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, FinalInputBam=FinalInputBam_path, bam_final=bamFinal_path, Tmp=self.Tmp)
        CMD_8_2 = "{JAVA} -jar {PicardDir}/BuildBamIndex.jar INPUT={bam_final} OUTPUT={bam_final_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_final=bamFinal_path, bam_final_idx=bamFinalIndex_path, Tmp=self.Tmp)
        print("\n%s\n>>> Executing command:\n%s" % (Step8, CMD_8_1))
        print("\n>>> Executing command:\n%s\n" % CMD_8_2)
        call(CMD_8_1, shell=True)
        call(CMD_8_2, shell=True)





"""
_ Log ____________________________________________________________________________

2017-04-27
    *1) Copy '*_dup.metrics' to 'Report' dir, but I haven't done it
    2) Step 7 didn't finish, view the 'knownSitesDBsnp' to find out what happens

2017-04-28
    1) Finish coding, tested locally, but there are some problems on the server #6

2017-05-02
    1) Server #6 issue due to python version(need python3, I guess that python2 can
     not call the function before define it), solved
    2) Finish Server #6 testing, worked well
    3) No finish check now

2017-05-03
    *1) '*_Final.bam' is empty, find the problem, maybe sample is too small
    2) Solved the problem above, Step1 path define in a wrong way
    3) Finish Server #6 testing, worked well

__________________________________________________________________________________
"""

"""
_ Steps of Picard and GATK Bam preparation _______________________________________

2017-04-28

    # Step 1 Picard.       BAM
    # Step 2 Picard.       Sort
    # Step 3 Picard.       Mark Duplicates
    # Step 4 Picard.       Add Reads Group
    # Step 5 GATK/Picard.  Split 'N' Trim
    # Step 6 GATK.         Realignment Around the INDLEs
    # Step 7 GATK.         Base Quality Score Recalibration
    # Step 8 Picard.       Final Output

__________________________________________________________________________________
"""
