Description = """

_ Information ____________________________________________________________________________

    Name         : Settings_SNP_mRNA
    Description  : Use for storing variety of settings, including path and process numbers.
                   Only for Server #6 now.
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
    Finish Date  : 2017-04-13
__________________________________________________________________________________________

"""



# Species database path set
species_dict = {

    # Arabidopsis TAIR10
    "Arabidopsis" :
        {
            "GenomeSTAR": "",
            "GTF": "",
            "Genome": "",
            "dbSNP": "",
            "AnnovarDB": "",
            "AnnovarBuild": "TAIR10",
        },

    # Mouse mm10
    "Mouse" :
        {
            "GenomeSTAR"   : "/home/pub/database/Mouse/mm10/STAR",
            "GTF"          : "/home/pub/database/Mouse/mm10/genes_rmchr.gtf",
            "Genome"       : "/home/pub/database/Mouse/mm10/mm10.fa",
            "dbSNP"        : "/home/pub/database/Mouse/mm10/snp/dbsnp.mm10.vcf",
            "AnnovarDB"    : "/home/pub/database/Mouse/mm10/Annotation",
            "AnnovarBuild" : "mm10",
        },

    # Human GRCh37/hg19
    "Human" :
        {
            "GenomeSTAR"   : "/home/pub/database/Human/hg19/genome/STAR_db",
            "GTF"          : "/home/pub/database/Human/hg19/gene/genes.nochr.gtf",
            "Genome"       : "home/pub/database/Human/hg19/genome/hg19.fa",
            "dbSNP"        : "/home/pub/database/Human/hg19/snp/dbsnp_137.hg19.vcf",
            "InDel"        : "/home/pub/database/Human/hg19/snp/1000G_phase1.indels.hg19.vcf",
            "AnnovarDB"    : "/home/pub/database/Human/hg19/Annotation",
            "AnnovarBuild" : "hg19",
        }
}


# Software settings
software_dict = {

    # Software path set
    "Tmp"        : "/home/tmp",
    "STAR"       : "/home/xudl/soft/STAR/bin/Linux_x86_64_static/STAR",
    "JAVA"       : "/usr/bin/java",
    "GATK"       : "/home/pub/software/GATK3/GenomeAnalysisTK.jar",
    "PicardDir"  : "/home/pub/software/GATK2/picard",
    "Samtools"   : "/home/pub/software/samtools-1.3.1/bin/samtools",
    "VarScan"    : "/home/pub/software/varscan/VarScan.v2.3.9.jar",
    "AnnovarDir" : "/home/pub/software/annovar",
    "BlastDir"   : "/home/pub/software/blast/bin",

    # Processes/Threads of softwares
    "Mapping"    : [5,30],      # 1st: processes of STAR programme numbers ; 2rd: threads of STAR
    "GATK"       : 3,           # Threads for 'dataPre' GATK
    "Calling"    : 20,
    "Genotyping" : 40,
    "Analysis"   : 40,

}

"""
_ Log _____________________________________________________________________________

2017-04-26
    1) Revised argument input part
    2) Revised 'software_dict', all process/thread parameter shift from character to integer
___________________________________________________________________________________

"""