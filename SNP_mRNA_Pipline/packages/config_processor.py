Description = """

_ Information ____________________________________________________________________
 Name         : ConfigProcessor_SNP_mRNA
 Description  : Produce 'config.ini' and 'run.ini' for
                Whole Transcription Sequecing(WTS) mRNA SNP pipline,
                using WTS pipline's 'config.txt'
 Author       : Hwx
 Version      : V4
 Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-15
___________________________________________________________________________________

"""



# Test pathes(Windows 10)
OPT_dir = "C:\\Users\\GiantStone_Hwx\\PycharmProjects\\Playground"
configOPT_path = "%s\\config.ini" % OPT_dir
runOPT_path = "%s\\run.ini" % OPT_dir
WTS_cfg_path = "WTS_config.txt"


import os
import re



# _ 1. Process the WTS config and get Info ___________________________________
def WTS_cfg(WTS_cfg_path):
    with open(WTS_cfg_path, "r") as WTS_config:

        WTS_cfg_dict = {
            "project_dir": "",
            "report_dir": "",
            "raw_data_dir": "",
            "sample": "",
            "organ": "",
            "group": [],
        }

        # Get WTS config information and store in dictionary 'WTS_cfg_dict'
        for l in WTS_config:
            if l.startswith("project"):
                WTS_cfg_dict["project_dir"] = re.split(" |\t", l)[-1].strip()
            elif l.startswith("report"):
                WTS_cfg_dict["report_dir"] = re.split(" |\t", l)[-1].strip()

            elif l.startswith("raw_data"):
                WTS_cfg_dict["raw_data_dir"] = re.split(" |\t", l)[-1].strip()

            elif l.startswith("sample"):
                WTS_cfg_dict["sample"] = re.split(" |\t", l)[-1].strip()

            elif l.startswith("organ"):
                WTS_cfg_dict["organ"] = re.split(" |\t", l)[-1].strip()

            else:
                if len(l) > 1:
                    WTS_cfg_dict["group"].append(l.strip())

    SNPoutput_dir = os.path.join(WTS_cfg_dict["project_dir"], "mRNA/SNP")
    if not os.path.exists(SNPoutput_dir):
        os.makedirs(SNPoutput_dir)

    return WTS_cfg_dict, SNPoutput_dir


# _ 2. Produce SNP_mRNA_Pipline 'config.ini'______________________________________________________
def configini(WTS_cfg_dict, SNPoutput_dir):

    output_path = SNPoutput_dir + "/config.ini"

    # Oupput 'config.ini' for SNP pipline
    with open(output_path, "w") as cfg:

        print("\nContent of 'config.ini' for SNP pipline:")
        print("_________________________________________")

        # Group INFO
        for gp in WTS_cfg_dict["group"]:
            gp = re.split(" |\t|;", gp)
            gpInfo = []
            for i in gp:
                if i != "":
                    gpInfo.append(i)

        # Other INFO
        Rawdata  = WTS_cfg_dict["raw_data_dir"]
        Output   = WTS_cfg_dict["project_dir"] + "/mRNA/SNP"
        Report   = WTS_cfg_dict["report_dir"] + "/mRNA/06_SNP"
        Species  = WTS_cfg_dict["organ"]
        Samples  = ""
        for s in WTS_cfg_dict["sample"].split(","):
            Samples += s + "\n"

        # Pathes of '=.bed' files
        bed_dict = {

            "human": "/home/pub/database/Human/hg19/bed/human_exons_realign.bed",
            "mouse": "/home/hwx/reference/mm10.bed",
            "arabidopsis": "/home/hwx/reference/Arabidopsis/TAIR10/AnnovarDB/TAIR10.bed",

        }

        # Choose '=bed' by species
        if Species.lower() == "human":
            Bed_path = bed_dict["human"].capitalize()

        elif Species.lower() == "mouse":
            Bed_path = bed_dict["mouse"].capitalize()

        elif Species.lower() == "arabidopsis":
            Bed_path = bed_dict["arabidopsis"].capitalize()

        # You can see the config dictionary structure here
        config_dict = {

            "section_1": {
                "1_title": "### Path Configuration",
                "2_": "case        = %s" % gpInfo[3],
                "3_": "control     = %s" % gpInfo[2],
                "4_": "FastqDir    = %s" % Rawdata,
                "5_": "OutputDir   = %s" % Output,  # Consist with WTS mRNA pipline
                "6_": "Report      = %s" % Report,  # Consist with WTS mRNA pipline
            },

            "section_2": {
                "1_title": "### Species Configuration",
                "2_": "Species     = %s" % Species.capitalize(),
            },

            "section_3": {
                "1_title": "### Section BED",
                "2_": "Bed         = %s" % Bed_path,
            },

            "section_4": {
                "1_title": "### Samples Configuration",
                "2_samples": "%s" % Samples,
            },

        }

        # Sort the congfig dictinary, and the result is a list, note here
        config_list = sorted(config_dict.items(), key=lambda d: d[0])

        for i in config_list:
            for j in i:

                # Skip key_value "section_=" and start a new line
                if isinstance(j, str):

                    # Format adjustment
                    if j.split(("_"))[-1] == str(1):
                        print("")
                        continue
                    cfg.write("\n")
                    print("")
                    continue

                j = sorted(j.items(), key=lambda d: d[0])  # Sort the information specific order
                # Final output
                for l in j:
                    cfg.write(l[1] + "\n")
                    print(l[1])

        return config_dict


# _ 3. Produce SNP_mRNA_Pipline 'run.ini' _______________________________________________________________
def runini(WTS_cfg_dict, SNPoutput_dir):

    output_path = SNPoutput_dir + "/run.ini"

    # Output the 'run.ini'
    with open(output_path, "w") as run:

        print("\nContent of 'run.ini' for SNP pipline:")
        print("_____________________________________\n")

        for gp in WTS_cfg_dict["group"]:
            gp = re.split(" |\t|;", gp)
            gpInfo = []
            for i in gp:
                if i != "":
                    gpInfo.append(i)

            RUN_para      = gpInfo[1] + "_vs_" + gpInfo[0]  # Group name: group1_vs_group2
            Case_para     = gpInfo[3]                       # Case samples: 5_1_leaves_1, 5_1_leaves_2
            Control_para  = gpInfo[2]                       # Case samples: Ler_leaves_1, Ler_leaves_2
            Model_para    = "Dominance"                     # Gene limited calculation related, default: Dominance
            Report_para   = "All"                           # Report model, default: All

            Freq_Alt_1000g_para     = str(0.01)  # 1000Genome database threshold
            ExAC03_para             = str(0.1)   # ExAC03 database threshold
            GENESKYDBHITS_Freq_para = str(0.05)  # GENESKYDBHITS database threshold

            # Human 'run.ini' config
            human_dict = {

                "::RUN "               : RUN_para,
                "Case:"                : Case_para,
                "Control:"             : Control_para,
                "Freq_Alt (1000g):"    : Freq_Alt_1000g_para,
                "ExAC03:"              : ExAC03_para,
                "GENESKYDBHITS_Freq:"  : GENESKYDBHITS_Freq_para,
                "Model:"               : Model_para,
                "Report:"              : Report_para,

            }

            # Other species 'run.ini' config
            other_dict = {

                "::RUN "    : RUN_para,
                "Case:"     : Case_para,
                "Control:"  : Control_para,
                "Model:"    : Model_para,
                "Report:"   : Report_para,

            }

            # Decide which config to use
            Species = WTS_cfg_dict["organ"]
            if "human" in Species.lower():
                run_dict = human_dict
            else:
                run_dict = other_dict

            write_list = sorted(run_dict.items(), key=lambda d: d[0])  # Learn from http://jingyan.baidu.com/article/75ab0bcbeaf643d6874db249.html
            for item in write_list:
                run.write(item[0] + item[1] + "\n")
                print(item[0] + item[1])
            run.write("\n")
            print("\n")

        return run_dict



# _ 0. When use this script alone ________________________________________
if __name__ == "__main__":

    import sys

    # Obtain pathes from command line(Linux)
    try:
        WTS_cfg_path    = sys.argv[1]
        OPT_dir         = sys.argv[2]
        configOPT_path  = "%s/config.ini" % OPT_dir
        runOPT_path     = "%s/run.ini" % OPT_dir

    except:
        print("""
        Usage:
            python %s <WTSconfig_path> <Output_path>
        """) % __file__
        exit()


    WTS_cfg_dict, SNPoutput_dir = WTS_cfg(WTS_cfg_path)  # Obtain sample and group information form WTS 'config.txt'
    configini(WTS_cfg_dict, SNPoutput_dir)  # Produce 'config.ini' for mRNA SNP pipline
    runini(WTS_cfg_dict, SNPoutput_dir)  # Produce 'run.ini' for mRNA SNP pipline

"""
_ Example _________________________________________________________________________

1.
===================================================================================
project    /home/hwx/work/RNA_seq/WTS_mRNA_17B0206A/
report     /home/hwx/work/RNA_seq/WTS_mRNA_17B0206A/work_path/report_new
raw_data   /home/pub/project/Transcriptome/17B0206A
sample     5_1_leaves_1,5_1_leaves_2,Ler_leaves_1,Ler_leaves_2
organ      Arabidopsis

Ler_1 5_1_1 Ler_leaves_1;5_1_leaves_1
Ler_2 5_1_2 Ler_leaves_2;5_1_leaves_2
Ler   5     Ler_leaves_1,Ler_leaves_2;5_1_leaves_1,5_1_leaves_2
===================================================================================


2.
===================================================================================
### Path Configuration
case        = 5_1_leaves_1,5_1_leaves_2
control     = Ler_leaves_1,Ler_leaves_2
FastqDir    = /home/pub/project/Transcriptome/17B0206A
OutputDir   = /home/hwx/work/RNA_seq/WTS_mRNA_17B0206A//mRNA/SNP
Report      = /home/hwx/work/RNA_seq/WTS_mRNA_17B0206A/work_path/report_new/mRNA/06_SNP

### Species Configuration
Species     = Arabidopsis

### Section BED
Bed         = /home/hwx/reference/Arabidopsis/TAIR10/AnnovarDB/TAIR10.bed

### Samples Configuration
5_1_leaves_1
5_1_leaves_2
Ler_leaves_1
Ler_leaves_2
===================================================================================


3.
===================================================================================
::RUN 5_1_1_vs_Ler_1
Case:5_1_leaves_1
Control:Ler_leaves_1
Model:Dominance
Report:All

::RUN 5_1_2_vs_Ler_2
Case:5_1_leaves_2
Control:Ler_leaves_2
Model:Dominance
Report:All

::RUN 5_vs_Ler
Case:5_1_leaves_1,5_1_leaves_2
Control:Ler_leaves_1,Ler_leaves_2
Model:Dominance
Report:All
===================================================================================

___________________________________________________________________________________



_ Important Information ______________________________________________________________

1. Server #6
Human_bed = "/home/pub/database/Human/hg19/bed/human_exons_realign.bed"
Mouse_bed = "/home/hwx/reference/mm10.bed"
Arabidopsis_bed = "/home/hwx/reference/Arabidopsis/TAIR10/AnnovarDB/TAIR10.bed"

___________________________________________________________________________________



_ Log _____________________________________________________________________________

2017-04-14
    1) Revised argument input part

2017-04-15
    1) Split name and value in 'WTS_cfg' part

2016-04-21
    1)

___________________________________________________________________________________

"""
