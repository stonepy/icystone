"""
    Compare Crawl results of the NCBI 'Gene Search' and '*_refGene.txt'
"""


input_path  = "NCBI_GeneSearch.txt"
output_path = "GeneFiltered_List.txt"

refGene_path = "hg19_refGene.txt"



with open(refGene_path, "r") as ref:

    refGene_dict = {}

    for l in ref:
        l_split = l.split("\t")
        refGene_dict[l_split[12]] = None


with open(input_path, "r") as inf:


    outf = open(output_path, "w")
    outf.write("Gene ID\tAvailable Aliases\n")

    GeneAliases_dict = {}

    for l in inf:

        if "Gene ID" in l:
            continue

        l_split = l.split("\t")
        ID  = l_split[0]
        Ali = l_split[1]

        GeneAliases_dict[ID] = ""

        for a in Ali.split(", "):

            a = a.strip()

            if a in refGene_dict:
                GeneAliases_dict[ID] += a + ", "


    for key in GeneAliases_dict:
        outl = key + "\t" + GeneAliases_dict[key].strip(", ") + "\n"
        outf.write(outl)
        print(outl)



    outf.close()







"""
    Crawl results of the NCBI 'Gene Search'
    Target Infomation: "Gene ID", "Alliases"
"""



from urllib import request

import time
import re



output_path = "NCBI_GeneSearch.txt"
input_path  = "Gene_List.txt"


outf = open(output_path, "w")
outf.write("Gene\tAliases\n")
outf.close()


def html_parser(gene_list):

    def parser(gene):

        gene = gene.strip()
        address = "https://www.ncbi.nlm.nih.gov/gene/?term=%s+human" % gene

        print("Request the website: %s\n" % address)
        with request.urlopen(address) as html:
            # with open("ncbi_gene.html", "r") as html:

            table = []
            tag = ["<td>", "</td>", "<td", "td>"]

            for l in html:
                l = str(l)
                for t in tag:
                    if t in l:
                        table.append(l)

            gene_table = list(set(table))[0]
            table_split = re.split("<td>|</td>|<td|td>", gene_table)
            print("Got html and finished processing.\n")

            Aliases = ""

            Aliases += table_split[1].split("""</a></div><span class="gene-id">""")[-2].split(">")[-1] + ", "
            if "human" in table_split[3]:
                Aliases += table_split[7]

            Aliases += table_split[11].split("""</a></div><span class="gene-id">""")[-2].split(">")[-1] + ", "
            if "human" in table_split[13]:
                Aliases += table_split[17]

            outl = gene + "\t" + Aliases.strip(", ") + "\n"
            outf.write(outl)
            print("Got Infomation:  " + outl + "\n")
            print(len("Got Infomation:  " + outl + "\n") * "-")


    with open(output_path, "w") as outf:

        outf.write("Gene ID\tAliases\n")
        for gene in gene_list:
            try:
                parser(gene)
                time.sleep(0)

            except Exception as e:
                print("Encounter Problem: %s\nNow retry ...\n" % e)
                try:
                    time.sleep(1)
                    parser(gene)
                except Exception as e:
                    print("Encounter Problem: %s\n" % e)



if __name__ == '__main__':

    with open(input_path, "r") as inf:

        gene_list = []
        for i in inf:
            gene_list.append(i)


    html_parser(gene_list)






"""
    Download database from 'Cosmic Drug Sensitivity' FTP, Demo
"""

import urllib.request
import time
import re
from subprocess import call

address = "ftp://ftp.sanger.ac.uk/pub4/cancerrxgene/releases/release-6.0/"

with urllib.request.urlopen(address) as response:

    for l in response:
        l = l.strip()
        filename = re.split("\t| |'", str(l))[-1]
        cmd = "wget %s%s &" % (address, filename)
        print(filename)
        call(cmd, shell=True)
        time.sleep(2)




