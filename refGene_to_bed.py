"""
- Information --------------------------------------------------------------------
 Name         : refGene_to_bed
 Description  : Transform '*_refGene.txt' to 'TAIR10.bed'
 Formulation  : None
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Windows10 Home CN, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-24
-----------------------------------------------------------------------------------
"""



import pandas as pd


path_refGene   = "TAIR10_refGene.txt"
path_BedOutput = "TAIR10.bed"

df_refGene   = pd.read_table(path_refGene)

with open(path_BedOutput, "w") as bed:

    for index, row in df_refGene.iterrows():
        iso   = row[1]
        chr   = row[2]
        ori   = row[3]
        start = row[9].split(",")[:-1]
        end   = row[10].split(",")[:-1]

        n = 0
        for coord in zip(start, end):
            print(coord)
            n += 1
            iso_n = iso + str(n)
            l = "\t".join([str(chr), str(coord[0]), str(coord[1]), str(ori), iso_n]) + "\n"
            bed.write(l)





# print(df_refGene)




