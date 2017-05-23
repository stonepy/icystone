import time
import sys


try:
    if len(sys.argv[1:]) == 3:
        reference_path, output_name, blastRes_path = sys.argv[1:]

    elif len(sys.argv[1:]) == 4:
        reference_path, output_name, blastRes_path, bowtieRes_path = sys.argv[1:]

    else:
        print(
        """
            Usage:

                python %s <Reference> <Output_Name> <Blast_Result> <Optional: Bowtie2_Result>

        """ % __file__)

    if not reference_path:
        raise

except Exception as e:

    print(e)

    try:
        blastRes_path   = "1_10000.blast.tsv"
        bowtie2Res_path = "1_10000.blast.tsv"
        reference_path  = "hg19-tRNAs.fa"
        output_name     = "aligned_segments"

    except Exception as e:
        print(e)
        exit()


def reference_seqMerge():
    ref_dict = {}
    fa_tmp   = None
    with open(reference_path, "r") as reference:
        for l in reference:

            l = l.strip()

            if l.startswith(">"):
                if fa_tmp:
                    ref_dict[l] = fa_tmp
                    fa_tmp = None

            else:
                try:
                    fa_tmp += l

                except Exception:
                    fa_tmp  = l

    return ref_dict



# There is something need to be fixed ===
# =======================================
def blast():
    with open(output_name+".blast.fa", "w") as res_fa:

        blastRes = open(blastRes_path, "r")
        blastRes_dict = {}

        for bl in blastRes:
            bl_spl  = bl.strip().split("\t")
            bl_id   = bl_spl[1]
            sbj_start = int(bl_spl[8])
            sbj_end   = int(bl_spl[9])




            for seq_id in ref_dict.keys():
                if bl_id in seq_id:
                    seq_tmp = ref_dict[seq_id]
                    faLen   = len(ref_dict[seq_id])

                    if sbj_start > sbj_end:
                        sbj_start = faLen - sbj_start + 1
                        sbj_end   = faLen - sbj_end + 1
                        seq_align  = seq_tmp[::-1][sbj_start:sbj_end][::-1]


                    else:
                        seq_align  = seq_tmp[sbj_start:sbj_end]


                    try:
                        blastRes_dict[bl_id].append([sbj_start,sbj_end,seq_align])

                    except Exception:
                        blastRes_dict[bl_id] = []
                        blastRes_dict[bl_id].append([sbj_start,sbj_end,seq_align])



        blastRes.close()
        for i in blastRes_dict.items():
            print(i)
# =======================================


def bowtie():
    with open(output_name+".bowtie2.fa", "w") as res_fa:

        bowtie2Res = open(bowtie2Res_path, "r")

        id_tmp  = None
        seq_tmp = None

        for bo in bowtie2Res:

            bo_spl  = bo.strip().split("\t")
            bo_id   = None

            sbj_start = None
            sbj_end   = None

            for ref in ref_list:

                ref = ref.strip()

                if ref.startswith(">"):

                    if id_tmp:
                        faLen = len(seq_tmp)
                        if sbj_start > sbj_end:

                            rsbj_start = faLen - sbj_start + 1
                            rsbj_end   = faLen - sbj_end + 1
                            fa_tmp = seq_tmp[::-1][rsbj_start:rsbj_end]

                        else:
                            fa_tmp = ref[sbj_start:sbj_end]

                        res_fa.write("%s\t%s\n" % (id_tmp, fa_tmp))

                        id_tmp  = None
                        seq_tmp = None

                    elif bl_id in ref:
                        id_tmp = bl_id


                elif not ref.startswith(">"):
                    try:
                        seq_tmp += ref
                    except Exception:
                        seq_tmp  = ref



        blastRes.close()


    pass








if __name__ == "__main__":
    ref_dict = reference_seqMerge()


    blast()
    # bowtie()
