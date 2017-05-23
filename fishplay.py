import time
import sys


def get_args():

    if len(sys.argv[1:]) > 3:
        reference_path, blastRes_path, output_path = sys.argv[1:]
        return reference_path, blastRes_path, output_path
    else:
        print(
    """
    \n
        Usage:

            python %s <Reference> <Blast_Result> <Output_Name>

    """ % __file__)


try:
    reference_path, blastRes_path, output_path = get_args()
    if not reference_path:
        raise

except Exception:
    blastRes_path  = "1_10000.blast.tsv"
    reference_path = "hg19-tRNAs-adjust.fa"
    output_path    = "aligned_segments.fa"



def blast():
    with open(output_path, "w") as res_fa:

        blastRes  = open(blastRes_path, "r")
        reference = open(reference_path, "r")

        ref_list = []
        id_tmp = None
        fa_tmp = None


        for l in reference:
            ref_list.append(l.strip())

        for bl in blastRes:

            bl_spl  = bl.strip().split("\t")
            bl_id   = bl_spl[1]

            sbj_start = int(bl_spl[8])
            sbj_end   = int(bl_spl[9])

            for ref in ref_list:

                if bl_id in ref:
                    id_tmp = bl_id
                    continue

                if id_tmp:

                    faLen = len(ref)
                    if sbj_start > sbj_end:

                        rsbj_start = faLen - sbj_start + 1
                        rsbj_end   = faLen - sbj_end + 1
                        fa_tmp = ref[::-1][rsbj_start:rsbj_end]

                    else:
                        fa_tmp = ref[sbj_start:sbj_end]

                    res_fa.write("%s\t%s\n" % (id_tmp, fa_tmp))

                    id_tmp = None


        blastRes.close()
        reference.close()


def bowtie():
    pass



if __name__ == "__main__":

    blast()
    bowtie()