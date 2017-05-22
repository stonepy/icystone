blastRes_path  = "1_1000.blast.tsv"
reference_path = "hg19-tRNAs-adjust.fa"

output_path = "aligned_segments.fa"


with open(output_path, "w") as fa:

    blastRes  = open(blastRes_path, "r")
    reference = open(reference_path, "r")

    for bl in blastRes:
        bl_id = bl.split("\t")[1]

        for ref in reference:
            ref_id = ref.split(" ")[0]


            if not ref.startswith(">"):
                continue

            print(ref_id)
            print()


            if bl in ref:
                print(bl)





    blastRes.close()
    reference.close()