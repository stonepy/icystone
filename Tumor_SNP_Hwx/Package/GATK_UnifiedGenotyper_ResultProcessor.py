
# _ Information ________________________________________________________________________

__Name__           = """ GATK_UnifiedGenotyper_ResultProcessor """
__Description__    = """ \n This Script is developed for processing GATK_UnifiedGenotyper results \n """
__Author__         = """ Hwx """
__Version__        = """ 1 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-06-05"""
__LastModificate__ = """ 2017-06-06"""
__Notes__          = """ None """

# _ Information ________________________________________________________________ End ___



# _ Packages ___________________________________________________________________________

import argparse

# _ Packages ___________________________________________________________________ End ___



# _ Arguments __________________________________________________________________________

def get_args():
    parser = argparse.ArgumentParser(description=__Description__)

    # For 'Tumor and Normal comparation'
    parser.add_argument("-VC", "--VCF_Comparation", help="Choose this option to choose different variant sites of Tumor and Normal VCF results of GATK-UnifiedGenotyper directly. (Use this option with '-t', '-n', 'o' options)", action="store_true")
    parser.add_argument("-t", "--VCF_tumorPATH", help="Provide path of Tumor VCF result of GATK-UnifiedGenotyper. (Use this option with '-VC' option)")
    parser.add_argument("-n", "--VCF_normalPATH", help="Provide path of Normal VCF result of GATK-UnifiedGenotyper. (Use this option with '-VC' option)")
    parser.add_argument("-o", "--VCF_outputDIR", help="Provide Directory of compared output VCF result of GATK-UnifiedGenotyper. (Use this option with '-VC' option)")

    # For 'Filtering out the normal sites in VCF file'
    parser.add_argument("-VF", "--VCF_Filter", help="Choose this option to filter the VCF result of GATK-UnifiedGenotyper, output VCF containing Variants. (Use this option with '-vi' and'-Vo' options)", action="store_true")
    parser.add_argument("-Vi", "--VCF_inputPATH", help="Provide path of VCF result of GATK-UnifiedGenotyper. (Use this option with '-VF' option)")
    parser.add_argument("-Vo", "--VCF_outputPATH", help="Provide filtered path of VCF result of GATK-UnifiedGenotyper. (Use this option with '-VF' option)")

    parser.add_argument("-p", "--nProcess", help="Numbers of processes")

    args = parser.parse_args()

    return args

# _ Arguments __________________________________________________________________ End ___



# // Main //////////////////////////////////////////////////////////////////////////////

def vcf_filter(VCF_inputPath, VCF_outputPath):
    with open(VCF_inputPath, "r") as Ivcf:

        Ovcf = open(VCF_outputPath, "w")

        for l in Ivcf:

            if l.startswith("#"):
                Ovcf.write(l)

            else:
                l_split = l.split("\t")
                if l_split[4] != ".":
                    Ovcf.write(l)

        Ovcf.close()


def TumorNormal_VCFcomparation(VCF_tumorPATH, VCF_normalPATH, VCF_outputDIR):

    TumorOutputPATH  = VCF_outputDIR + "/Tumor_unique.vcf"
    NormalOutputPATH = VCF_outputDIR + "/Normal_unique.vcf"

    # 'To' stands for 'tumor output'; 'No' stands for 'Normal output'
    ToVcf = open(TumorOutputPATH, "w")
    NoVcf = open(NormalOutputPATH, "w")

    # 'Ti' stands for 'tumor input'; 'Ni' stands for 'Normal input'
    TiVcf = open(VCF_tumorPATH, "r")
    NiVcf = open(VCF_normalPATH, "r")



    # ___ Version 2 _____________

    def v2():
        pass

    # ___ Version 2 ______ End ___




    # ___ Version 1 _____________

    def v1():
        while True:

            try:
                tumorL   = next(TiVcf)
                normarlL = next(NiVcf)
            except:
                break

            if tumorL.startswith("#"):
                ToVcf.write(tumorL)
                NoVcf.write(normarlL)

            elif tumorL.split("\t")[4] == normarlL.split("\t")[4]:
                    continue

            else:
                ToVcf.write(tumorL)
                NoVcf.write(normarlL)

    # ___ Version 1 ______ End ___



    v2()

    TiVcf.close()
    NiVcf.close()

    ToVcf.close()
    NoVcf.close()



# // Main ////////////////////////////////////////////////////////////////////// End ///



# _ Execution Control __________________________________________________________________

if __name__ == "__main__":
    args = get_args()

    # If user chosed '-VC' option, execute 'TumorNormal_VCFcomparation' function
    if args.VCF_Comparation:
        TumorNormal_VCFcomparation(args.VCF_tumorPATH, args.VCF_normalPATH, args.VCF_outputDIR)
        exit()

    # If user chosed '-VF' option, execute 'vcf_filter' function
    if args.VCF_Filter:
        vcf_filter(args.VCF_inputPATH, args.VCF_outputPATH)
        exit()


# _ Execution Control __________________________________________________________ End ___





# - Log --------------------------------------------------------------------------------
Log = """

2017-06-05
    1) Start this script
    2) Built 2 functions:
        1> vcf_filter
        2> TumorNormal_VCFcomparation

2017-06-06
    1) Tested, works !
    2) 'TumorNormal_VCFcomparation' add new condition

"""
# - Log ------------------------------------------------------------------------ End ---
