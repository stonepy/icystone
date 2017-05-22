input_path  = "hg19-tRNAs.fa"
output_path = "hg19-tRNAs-adjust.fa"

with open(input_path, "r") as f:

    g = open(output_path, "w")

    tmp_fa = ""

    for l in f:

        if l.startswith(">"):
            if len(tmp_fa) > 0:
                g.write(tmp_fa + "\n")
                g.write(l)
                tmp_fa = ""

            else:
                g.write(l)

        elif not l.startswith(">"):
            tmp_fa += l.strip()


    g.close()