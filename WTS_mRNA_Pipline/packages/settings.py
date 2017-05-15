Info = """

_ Information ____________________________________________________________________________

    Name         : Settings_SNP_mRNA
    Description  : Use for storing variety of settings, including path and process numbers.
                   Only for Server #6 now.
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
    Finish Date  : 2017-05-
__________________________________________________________________________________________

"""


from os.path import join as pjoin



# Species database path set
Reference_dict = {

    # Arabidopsis TAIR10
    "Arabidopsis" :
        {

        },

    # Mouse mm10
    "Mouse" :
        {

        },

    # Human GRCh37/hg19
    "Human" :
        {

        }
}


# Software settings
Software_dict = {


    "SoftPATH"  :   "",

    "Python3"   : {
        "path"  : "/home/hwx/bin/virENV/python35_hwx/bin/python",
        "info"  : "This is the python3 in my directory",
    },

    "Python2"   :   {
        "path"  :   "/home/hwx/bin/virENV/python27_hwx/bin/python",
        "info"  :   "This is the python2 in my directory",
    },

    "R"         :   {
        "path"  : "/usr/bin/R",
        "info"  : "System default",
    },

    "Java"      :   {
        "path"  : "",
        "info"  : "",
    },

    "FastQC"    :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "iTools"    :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "Fastx_toolkit" :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "Trim_Galore"   :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "HISAT2"    :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "Samtools"  :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "Picard"    :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "RNA_SeQC"  :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

    "RSEQC"     :   {
        "path"  : "",
        "nProcess"  : "",
        "nThread"   : "",
        "info"  : "",
    },

}


# Result dir
ResultDIR = {
    "log"   :   "",

}


# Report dir
ReportDIR = {

}



"""
_ Log _____________________________________________________________________________

2017-05-12
    1)
___________________________________________________________________________________

"""
