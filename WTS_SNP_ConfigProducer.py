"""
- Information --------------------------------------------------------------------
 Name         : WTS_SNP_ConfigProducer
 Description  : Produce 'run.ini' for Whole Transcription Sequecing mRNA SNP pipline
 Formulation  : None
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Windows10 Home CN, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-0
-----------------------------------------------------------------------------------
"""



import re
import sys


# WTS_config_path = sys.argv[1]
# WTS_config_path = sys.argv[2]
ouputdir = "C:\\Users\\GiantStone-Hwx\\PycharmProjects\\Playground"
output_path = "%s\\run.ini" % ouputdir
WTS_config_path = "WTS_config.txt"

with open(WTS_config_path, "r") as WTS_config:

    WTS_cfg_dict = {
        "project_dir"   : "",
        "report_dir"    : "",
        "raw_data_dir"  : "",
        "sample"        : "",
        "organ"         : "",
        "group"         : [],
    }

    # Get WTS config information
    for l in WTS_config:
        if l.startswith("project"):
            WTS_cfg_dict["project_dir"]  = l.strip()

        elif l.startswith("report"):
            WTS_cfg_dict["report_dir"]   = l.strip()

        elif l.startswith("raw_data"):
            WTS_cfg_dict["raw_data_dir"] = l.strip()

        elif l.startswith("sample"):
            WTS_cfg_dict["sample"]       = l.strip()

        elif l.startswith("organ"):
            WTS_cfg_dict["organ"]        = l.strip()

        else:
            if len(l) > 1:
                WTS_cfg_dict["group"].append(l.strip())


# Output the 'run.ini'
with open(output_path, "w") as run:
    for g in WTS_cfg_dict["group"]:
        g  = re.split(" |\t|;", g)
        gl = []
        for i in g:
            if i != "":
                gl.append(i)

        RUN_para     = gl[1] + "_vs_" + gl[0]    # Group name: group1_vs_group2
        Case_para    = gl[3]                     # Case samples: 5-1-leaves-1, 5-1-leaves-2
        Control_para = gl[2]                     # Case samples: Ler-leaves-1, Ler-leaves-2
        Model_para   = "Dominance"               # Gene limited calculation related, default: Dominance
        Report_para  = "All"                     # Report model, default: All

        Freq_Alt_1000g_para     = str(0.01)    # 1000Genome database threshold
        ExAC03_para             = str(0.1)     # ExAC03 database threshold
        GENESKYDBHITS_Freq_para = str(0.05)    # GENESKYDBHITS database threshold

        # Human 'run.ini' config
        human_dict = {

            "::RUN "    : RUN_para,
            "Case:"     : Case_para,
            "Control:"  : Control_para,
            "Freq_Alt (1000g):"     : Freq_Alt_1000g_para,
            "ExAC03:"               : ExAC03_para,
            "GENESKYDBHITS_Freq:"   : GENESKYDBHITS_Freq_para,
            "Model:"    : Model_para,
            "Report:"   : Report_para,
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
        if "human" in WTS_cfg_dict["organ"].lower():
            write_dict = human_dict
        else:
            write_dict = other_dict

        write_dict = sorted(write_dict.items(), key=lambda d: d[0])    # Learn from http://jingyan.baidu.com/article/75ab0bcbeaf643d6874db249.html

        for item in write_dict:
            run.write(item[0] + item[1] + "\n")
        run.write("\n")



