"""
    Drug Sensitivity in Cancer database process
"""


input_path  = "senseDR.txt"
output_path = "senseDR.txt.xls"


import pandas as pd


df = pd.read_table(input_path)

target = df["targets"]


geneDict = {}
n = 0
for g in target:
    gene = g.split(",")
    for j in gene:
        n += 1
        geneDict[j.lstrip(" ")] = ""


for index,row in df.iterrows():

    for i in row[4].split(","):
        if i in geneDict:
            geneDict[i] += "%s : %s : %s ; " % (row[1], row[2], row[3])


with open(output_path, "w") as outf:

    outf.write("Gene Symbol\tDrug Name ; Synonyms ; Pathway Name\n")
    for key in geneDict:

        outl = key + "\t" + geneDict[key].strip(" ;") + "\n"
        outf.write(outl)



 




"""
    NovoDriver Genes process
"""


input_path  = "NovoDriverGene.txt"
output_path = "NovoDriverGene.xls"


import pandas as pd


df = pd.read_table(input_path)

geneList   = df["Gene Symbol"]
sourceList = df["Source"]

uniqueGene   = set(geneList)
uniqueSource = set(sourceList)

geneDict = {}
for i in uniqueGene:
    geneDict[i] = ""


outf = open(output_path, "w")

for index,row in df.iterrows():

    if "Gene Symbol" == row[0]:
        continue

    gene   = row[0]
    source = row[1]

    if gene in geneDict:
        geneDict[gene] += source + ","

outf.write("Gene Symbol\tSource\n")
for i in geneDict:

    outl = i + "\t" + geneDict[i].strip(",") + "\n"
    outf.write(outl)

outf.close()







"""
    CGC database process
"""


input_path  = "CGC.csv"
output_path = "CGC.xls"

with open(input_path, "r") as inf:

    outf = open(output_path, "w")

    title = "Gene\tTumor\n"
    outf.write(title)
    # print(title)


    next(inf)
    for l in inf:
        print(l)

        l_split = l.strip().split("\t")

        outl = l_split[0] + "\t"
        for i in l_split[1:]:
            outl += i + ","
        outl = outl.strip() + "\n"
        outf.write(outl)

    outf.close()
