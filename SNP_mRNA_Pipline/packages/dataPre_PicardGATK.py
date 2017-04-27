Description = """

_ Information ____________________________________________________________________

    Name         : dataPre_Picard_GATK_SNP_mRNA
    Description  : Prepare data for seeking INDEL/SNP with GATK programme
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_04_2
__________________________________________________________________________________


"""


from packages.process_manager import call_func
from packages.process_manager import multiP_1
from packages.checking        import branchDIR_check
from packages                 import settings
from subprocess               import call
import shutil
import time



class main:

    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

                              ================================================
                              |                                              |
                              |  Start prepare with Picard & GATK programme  |
                              |                                              |
                              ================================================


        %s
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
        self.Genome     = settings.species_dict[self.Species]         # Genome fasta file
        self.Tmp        = settings.software_dict["Tmp"]          #
        self.JAVA       = settings.software_dict["JAVA"]         #
        self.PicardDir  = settings.software_dict["PicardDir"]    #
        self.GATK       = settings.software_dict["GATK"]         #
        self.Samtools   = settings.software_dict["Samtools"]     #
        self.Threshold  = settings.software_dict["GATK"]         #

    """ _ Data preparation ________________________________________________________________________________________ """
    def run_module(self, sampleName):

        # If "dbSNP" and "InDel" exist, only human and mouse for the temporary
        if "dbSNP" in settings.software_dict[self.Species]:
            knownDBsnp     = "-known " + settings.software_dict[self.Species]["dbSNP"]
            knownSiteDBsnp = "-knownSite " + settings.software_dict[self.Species]["dbSNP"]
        if "InDel" in settings.software_dict[self.Species]:
            knownInDel     = "-known " + settings.software_dict[self.Species]["InDel"]

        # Make sure the directory for '*.bam' files exists
        BamDir = "%s/%s" % (self.OutputDir, sampleName)
        branchDIR_check(BamDir)


        # Step 1 Picard. BAM, convert '*.sam' with the '*.bam' file, results of STAR mapping _____________________________________
        sam_path = "%s/%s.step2.Aligned.out.sam" % (BamDir, sampleName)
        bam_path = "%s/%s.bam" % (BamDir, sampleName)

        CMD_1 = "more {sam} | {Samtool} view -bS -L {bed} -h -F 4 - > {bam}".format(sam=sam_path, Samtools=self.Samtools, bed=self.bed, bam=bam_path)
        print(CMD_1) # for testing
        call(CMD_1, shell=True)


        # Step 2 Picard. Sort, '*.bam' files sorting __________________________________________________________________
        bamSort_path      = "%s/%s_sort.bam" % (BamDir, sampleName)
        bamSortIndex_path = "%s/%s_sort.bai" % (BamDir, sampleName)

        CMD_2_1 = "{JAVA} -jar -Xmx6g {PicardDir}/SortSam.jar INPUT={bam} OUTPUT={bam_sort} SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam=bam_path, bam_sort=bamSort_path, Tmp=self.Tmp)
        CMD_2_2 = "{JAVA} -jar -Xmx6g {PicardDir}/BuildBamIndex.jar INPUT={bam_sort} OUTPUT={bam_sort_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_sort_idx=bamSortIndex_path, Tmp=self.Tmp)

        call(CMD_2_1, shell=True)
        call(CMD_2_2, shell=True)


        # Step 3 Picard. Mark Duplicates, mark duplicates in the '*.bam' file __________________________________________
        bamDup_path        = "%s/%s_sort_dup.bam" % (BamDir, sampleName)
        bamDupMetrics_path = "%s/%s_dup.metrics" % (BamDir, sampleName)     # Copy '*_dup.metrics' to 'Report' dir, but I don't do it
        bamDupIndex_path   = "%s/%s_sort_dup.bai" % (BamDir, sampleName)

        CMD_3_1 = "{JAVA} -jar -Xmx8g {PicardDir}/MarkDuplicates.jar INPUT=${bam_sort} OUTPUT={bam_dup} METRICS_FILE={bam_dup_metrics} REMOVE_DUPLICATES=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_dup=bamDup_path, bam_dup_metrics=bamDupMetrics_path, Tmp=self.Tmp)
        CMD_3_2 = "{JAVA} -jar -Xmx8g {PicardDir}/BuildBamIndex.jar INPUT={bam_dup} OUTPUT={bam_dup_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_dup=bamDup_path, bam_dup_idx=bamDupIndex_path, Tmp=self.Tmp)

        call(CMD_3_1, shell=True)
        call(CMD_3_2, shell=True)


        # Step 4 Picard. Add Reads Group, add reads group to the '*.bam' file ___________________________________________
        bamGroup_path      = "%s/%s_sort_dup_group.bam" % (BamDir, sampleName)
        bamGroupIndex_path = "%s/%s_sort_dup_group.bai" % (BamDir, sampleName)

        CMD_4_1 = "{JAVA} -jar -Xmx16g {PicardDir}/AddOrReplaceReadGroups.jar I={bam_dup} O={bam_group} SO=coordinate ID=$sample LB={sample} PL=illumina PU=barcode SM={sample} CREATE_INDEX=false VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_sort=bamSort_path, bam_dup=bamDup_path, bam_group=bamGroup_path, sample=sampleName, Tmp=self.Tmp)
        CMD_4_2 = "{JAVA} -jar -Xmx8g {PicardDir}/BuildBamIndex.jar INPUT={bam_group} OUTPUT={bam_group_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_group=bamGroup_path, bam_group_idx=bamGroupIndex_path, Tmp=self.Tmp)

        call(CMD_4_1, shell=True)
        call(CMD_4_2, shell=True)


        # Step 5 GATK/Picard. Split 'N' Trim, Split 'N' and trim from the '*.bam' file ________________________________
        bamTrim_path      = "%s/%s_sort_dup_group_trim.bam" % (BamDir, sampleName)
        bamTrimIndex_path = "%s/%s_sort_dup_group_trim.bai" % (BamDir, sampleName)

        CMD_5_1 = "{JAVA} -jar {GATK} -T SplitNCigarReads -R $Genome -I {bam_group} -o {bam_trim} -U ALLOW_N_CIGAR_READS -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_group=bamGroup_path, bam_trim=bamTrim_path)
        CMD_5_2 = "{JAVA} -jar -Xmx8 {PicardDir}/BuildBamIndex.jar INPUT={bam_trim} OUTPUT={bam_trim_idx} VALIDATION_STRINGENCY=LENIENT TMP_DIR={Tmp}".format(JAVA=self.JAVA, PicardDir=self.PicardDir, bam_trim=bamTrim_path, bam_trim_idx=bamTrimIndex_path, Tmp=self.Tmp)

        call(CMD_5_1, shell=True)
        call(CMD_5_2, shell=True)


        # Step 6 GATK, Realignment, realign around the INDLEs _________________________________________________________
        bamRealign_path          = "%s/%s_sort_dup_group_trim_realign.bam" % (BamDir, sampleName)
        bamRealignIntervals_path = "%s/%s_sort_dup_group_trim_realign.intervals" % (BamDir, sampleName)

        CMD_6_1 = "{JAVA} -jar {GATK} -l INFO -T RealignerTargetCreator -R {Genome} -I {bam_trim} -o {bam_realign_intervals} {knownDBsnp} {knownInDel} --validation_strictness LENIENT".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_trim=bamTrim_path, bam_realign_intervals=bamRealignIntervals_path, knownDBsnp=knownDBsnp, knownInDel=knownInDel)
        CMD_6_2 = "{JAVA} -jar {GATK} -l INFO -T IndelRealigner -R {Genome} -I {bam_trim} -o ${bam_realign} {knownInDel} -targetIntervals {bam_realign_intervals} --validation_strictness LENIENT".format(JAVA=self.JAVA, GATK=self.GATK, Genome=self.Genome, bam_trim=bamTrim_path, bam_realign=bamRealign_path, knownInDel=knownInDel, bam_realign_intervals=bamRealignIntervals_path)

        call(CMD_6_1, shell=True)
        call(CMD_6_2, shell=True)


        # Step 7 GATK, Base Quality Score Recalibration _______________________________________________________________
        bamRecalibrator_path      = "%s/%s_sort_dup_group_trim_realign_recalibrator.bam" % (BamDir, sampleName)
        bamRecalibratorIndex_path = "%s/%s_sort_dup_group_trim_realign_recalibrator.bai" % (BamDir, sampleName)
        recal_path                = "%s/%s_recal.table" % (BamDir, sampleName)

        CMD_7_1 = ""
        CMD_7_2 = ""

        call(CMD_7_1, shell=True)
        call(CMD_7_2, shell=True)

        # Step 8 Picard, Final




        # Finish Note __________________________________________________________________________________________________
        note_finish = """

                              =================================================
                              |                                               |
                              |  Finish prepare with Picard & GATK programme  |
                              |                                               |
                              =================================================


        %s
        """ % time.ctime()
        print(note_finish)





"""
_ Log _____________________________________________________________________________

2017-04-27
    *1) Copy '*_dup.metrics' to 'Report' dir, but I don't do it
    2) Step 7 didn't finish, view the 'knownSitesDBsnp' to find out what happens

___________________________________________________________________________________
"""

"""
_ Steps of Picard and GATK ________________________________________________________

2017-04-27



___________________________________________________________________________________
"""