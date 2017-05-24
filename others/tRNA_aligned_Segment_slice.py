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

        raise

except:

    print(">>> Use the default parameters\n")

    try:
        blastRes_path   = "1_10000.blast.tsv"
        bowtie2Res_path = "1_10000.blast.tsv"
        reference_path  = "hg19-tRNAs.fa"
        output_name     = "aligned_segments"

    except Exception as e:
        print(e)
        exit()


def reference_seqMerge(reference_path):
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

                except:
                    fa_tmp  = l

    return ref_dict


def blast(ref_dict):
    output_path = output_name + ".blast.trd"
    blastRes    = open(blastRes_path, "r")
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
                    seq_align = seq_tmp[::-1][sbj_start:sbj_end][::-1]
                else:
                    seq_align = seq_tmp[sbj_start:sbj_end]

                try:
                    blastRes_dict[bl_id].append([sbj_start,sbj_end,seq_align])
                except:
                    blastRes_dict[bl_id] = []
                    blastRes_dict[bl_id].append([sbj_start,sbj_end,seq_align])

    blastRes.close()
    format_output(output_path, ref_dict, blastRes_dict)



def format_output(output_path, Ref_dict, Res_dict):

    with open(output_path, "w") as fm_out:

        symbol      = "."
        space       = " "
        idBlock_len = 60
        out_dict    = {}

        for seq_id in Ref_dict.keys():
            for res_id in Res_dict.keys():
                ref_seq = Ref_dict[seq_id]

                if res_id in seq_id:
                    refSeq_len = len(ref_seq)
                    out_dict[res_id] = [ref_seq+"\n"]

                    for info in Res_dict[res_id]:
                        res_seq = info[2]
                        if info[0] > info[1]:
                            start = info[1]
                            end   = info[0]
                        else:
                            start = info[0]
                            end   = info[1]

                        resIdSeq = (start * symbol) + res_seq + ((refSeq_len - end) * symbol) + "\n"
                        out_dict[res_id].append(resIdSeq)

        for id in out_dict:
            id_len    = len(id)
            space_len = idBlock_len - id_len
            spaces    = space * space_len

            fm_out.write("\n\n")

            ref_line = True
            for l in out_dict[id]:

                if ref_line:
                    x = idBlock_len - len("Reference Sequence:")
                    outLine = "Reference Sequence:" + (space * x) + l
                    fm_out.write(outLine)
                    ref_line = False
                    continue

                outLine = id + spaces + l
                fm_out.write(outLine)
                print(outLine)


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

    ref_dict = reference_seqMerge(reference_path)
    blast(ref_dict)

    # bowtie(ref_dict)
