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
                    outf.write("Gene Skippd\n")
                    print("Encounter Problem: %s\n" % e)



if __name__ == '__main__':

    with open(input_path, "r") as inf:

        gene_list = []
        for i in inf:
            gene_list.append(i)


    html_parser(gene_list)

