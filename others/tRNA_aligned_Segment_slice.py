
Info = {
# _ Information ____________________________________________________________________

    "__Name"         : "tRNA_aligned_Segment_slice",
    "__Description"  : "Use for selecting the corresponding segments of tRNA reads\
                        aligned to the reference sequences",

    "__Author"       : "Hwx",
    "__Version"      : "V0",
    "__Dev Env"      : "Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0",
    "__Finish Date"  : "2017_05-24",
# __________________________________________________________________________________

}




import sys


try:
    if len(sys.argv[1:])   == 3:
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
        bowtieRes_path  = "1_tmp.sam"
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
                    fa_tmp      = None

            else:
                try:
                    fa_tmp += l
                except:
                    fa_tmp  = l

    return ref_dict


def blast(blastRes_path, ref_dict):
    output_path   = output_name + ".blast.trd"
    blastRes      = open(blastRes_path, "r")
    blastRes_dict = {}

    for bl in blastRes:
        bl_spl    = bl.strip().split("\t")
        bl_id     = bl_spl[1]
        sbj_start = int(bl_spl[8])
        sbj_end   = int(bl_spl[9])

        ref_search(blastRes_dict, bl_id, sbj_start, sbj_end)

    blastRes.close()
    format_output(output_path, ref_dict, blastRes_dict)


def bowtie(bowtieRes_path, ref_dict):
    output_path    = output_name + ".bowtie.trd"
    bowtieRes      = open(bowtieRes_path, "r")
    bowtieRes_dict = {}

    for bt in bowtieRes:
        bt_spl    = bt.strip().split("\t")
        bt_id     = bt_spl[2]
        sbj_start = int(bt_spl[3])
        sbj_end   = int(bt_spl[5].strip("M"))

        ref_search(bowtieRes_dict, bt_id, sbj_start, sbj_end)

    bowtieRes.close()
    format_output(output_path, ref_dict, bowtieRes_dict)


def ref_search(res_dict, res_id, sbj_start, sbj_end):

    for seq_id in ref_dict.keys():
        if res_id in seq_id:
            seq_tmp = ref_dict[seq_id]
            faLen   = len(ref_dict[seq_id])

            if sbj_start > sbj_end:
                sbj_start = faLen - sbj_start
                sbj_end   = faLen - sbj_end
                # Because the '*.SAM' file use 1-based coordinate system, but python use 0-postiton coordinate system, -1. When reverse the sequence and the position need to +1, offset -1
                seq_align = seq_tmp[::-1][sbj_start:sbj_end][::-1]
            else:
                # Because the '*.SAM' file use 1-based coordinate system, but python use 0-postiton coordinate system, substract 1
                seq_align = seq_tmp[sbj_start-1:sbj_end-1]

            try:
                res_dict[res_id].append([sbj_start-1, sbj_end-1, seq_align])
            except:
                res_dict[res_id] = []
                res_dict[res_id].append([sbj_start-1, sbj_end-1, seq_align])


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
                    refSeq_len       = len(ref_seq)
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
                    n        = idBlock_len - len("Reference Sequence:")
                    outLine  = "Reference Sequence:" + (space * n) + l
                    fm_out.write(outLine)
                    ref_line = False
                    continue

                outLine = id + spaces + l
                fm_out.write(outLine)

                # print(outLine)



if __name__ == "__main__":
    ref_dict = reference_seqMerge(reference_path)

    blast(blastRes_path, ref_dict)
    bowtie(bowtieRes_path, ref_dict)
