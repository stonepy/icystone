"""
- Information --------------------------------------------------------------------
 Name         :   lncRNA_mRNA_Database
 Description  :   Find the expression relationship between lncRNA and mRNA, finally
                   output the gtf files in different folders
 Author       :   Hwx
 Version      :   V1
 Dev Env      :   Red Hat 4.8.5-11, Python3.5.3, virtualenv15.1.0
 Finish Date  :   2017-02-20
-----------------------------------------------------------------------------------
"""



import pandas as pd
import time
import os
import shutil
import re



class main:

    def __init__(self):

        self.path_root   = "/home/daniel/PycharmProjects/fishPool/files/"
        self.path_output = self.path_root + "output/"

        try:
            os.makedirs(self.path_output)
        except:
            shutil.rmtree(self.path_output)
            os.makedirs(self.path_output)



    def lncRNA_flankLocus(self):

        lncRNA_locus_path = self.path_root + "lncRNA.locus.xls"

        # 10kbp wide flank
        flank_wide = 10000

        # Read raw lncRNA locus table
        df_lncLocus = pd.read_table(lncRNA_locus_path, usecols=["gene_id", "locus"])

        # Seperate lncRNA locus info from raw table
        id  = df_lncLocus["gene_id"]
        chr = df_lncLocus["locus"].map(lambda x: x.split(":")[0])
        start = df_lncLocus["locus"].map(lambda x: x.split(":")[1].split("-")[0])
        end   = df_lncLocus["locus"].map(lambda x: x.split(":")[1].split("-")[1])

        # Merge lncRNA info into a DataFrame and save to file
        df_lncLocus = pd.DataFrame([id, chr, start, end], index=["gene_id", "chr", "start", "end"]).T
        df_lncLocus.to_csv(self.path_output+"lncRNA_Locus.csv", index_label=None, index=None, sep="\t")

        # df_lncLocus = pd.read_table(self.path_output+"lncLocus.csv")

        # Calculate the flanking locus and merge into a DataFrame
        df_flankLocus = pd.DataFrame([id, chr]).T
        df_flankLocus["upStart"]   = df_lncLocus["start"].map(lambda x: int(x) - flank_wide)
        df_flankLocus["upEnd"]     = df_lncLocus["start"]
        df_flankLocus["downStart"] = df_lncLocus["end"]
        df_flankLocus["downEnd"]   = df_lncLocus["end"].map(lambda x: int(x) + flank_wide)

        # Save flanking locus info to file
        df_flankLocus.to_csv(self.path_output+"lncRNA_flankLocus.csv", index_label=None, index=None, sep="\t")

        # self.df_flankLocus = df_flankLocus



    def mRNA_locus(self):

        mRNA_locus_path   = self.path_root + "mRNA.locus.xls"
        mRNA_id_path      = self.path_root + "mRNA.id"

        # Read raw mRNA locus table
        df_mRNA_locus = pd.read_table(mRNA_locus_path, usecols=["gene_id", "locus"])
        list_mRNA_id  = pd.read_table(mRNA_id_path, usecols=[0],names=["gene_id"]).drop(0)

        # Select listed mRNA locus info
        df_mRNA_locusSelected = pd.merge(list_mRNA_id, df_mRNA_locus, on="gene_id")

        # Seperate mRNA locus info from raw table
        id  = df_mRNA_locusSelected["gene_id"]
        chr = df_mRNA_locusSelected["locus"].map(lambda x: x.split(":")[0])
        start = df_mRNA_locusSelected["locus"].map(lambda x: x.split(":")[1].split("-")[0])
        end   = df_mRNA_locusSelected["locus"].map(lambda x: x.split(":")[1].split("-")[1])

        # Merge mRNA info into a DataFrame and save to file
        df_mRNA_locusSelected = pd.DataFrame([id, chr, start, end], index=["gene_id", "chr", "start", "end"]).T
        df_mRNA_locusSelected.to_csv(self.path_output+"mRNA_selected_locus.csv", index_label=None, index=None, sep="\t")

        # self.df_mRNA_locusSelected = df_mRNA_locusSelected



    def lncRNA_flank_mRNA_Match(self):

        # Read result from func 'lncRNA_flankLocus()'
        df_lncRNA_flank_locus = pd.read_csv(self.path_output + "lncRNA_flankLocus.csv", sep="\t")
        # Read result from func 'mRNA_locus()'
        df_mRNA_locus = pd.read_csv(self.path_output + "mRNA_selected_locus.csv", sep="\t")

        # Corresponding relationship dictionary
        lncRNA_mRNA_dict = {}
        # Tranverse lncRNA
        for lncRNA_index, lncRNA_row in df_lncRNA_flank_locus.iterrows():

            # Tranverse selected mRNA
            for mRNA_index, mRNA_row in df_mRNA_locus.iterrows():

                # Chr equal. Note: [1][1] ~ chr, [1][2] ~ flank start_site, [1][5] ~ flank end_site
                if mRNA_row[1] == lncRNA_row[1]:

                    # mRNA start_site locates between lncRNA start_site and end_site
                    if mRNA_row[2] >= lncRNA_row[2] and mRNA_row[2] <= lncRNA_row[5]:

                        try:
                            lncRNA_mRNA_dict[lncRNA_row[0]].append(mRNA_row[0])
                        except:
                            lncRNA_mRNA_dict[lncRNA_row[0]] = [mRNA_row[0]]
                        # lncRNA_mRNA_dict = {
                        #     lncRNA_name : [mRNA_name, ...],
                        #     ...
                        # }


        # Somehow the result need to be transposed and write to file
        with open(self.path_output+"lncRNA_mRNA.txt", "w") as f:
            for item in lncRNA_mRNA_dict.items():
                l = item[0]
                for i in item[1]:
                    l += "\t" + i
                l = l + "\n"
                f.write(l)



    def lncRNA_mRNA_listSeperation(self):

        path_lncRNA_mRNA = self.path_output + "lncRNA_mRNA.txt"

        # Read lnc_mRNA corresponding table
        with open(path_lncRNA_mRNA, "r") as f:
            lncRNA_list = ""
            mRNA_list   = ""
            for l in f:
                lncRNA_list += l.split("\t")[0]+"\n"
                m = ""
                for i in l.split("\t")[1:]:
                    m += i + "\t"
                mRNA_list += m.strip("\t")

            with open(self.path_output+"lncRNA_selected_list.txt","w") as lnc_list:
                lnc_list.write(lncRNA_list)
            with open(self.path_output+"mRNA_selected_list.txt","w") as m_list:
                m_list.write(mRNA_list)



    def lncRNA_GTF(self):

        # Path
        path_lncRNA_gtf = self.path_root + "hg19_lncRNA.fmt.gtf"
        path_lncRNA_selected_list = self.path_output + "lncRNA_selected_list.txt"

        with open(path_lncRNA_gtf, "r") as lnc_gtf:
            with open(path_lncRNA_selected_list, "r") as lnc_list:
                lncs = []
                for l in lnc_list:
                    lncs.append(l.strip("\n"))

                lncRNA_gtf = ""
                for anno in lnc_gtf:
                    for lnc in lncs:
                        if lnc in anno:
                            lncRNA_gtf += anno

        try:
            os.makedirs(self.path_output + "lncRNA_GTF")
        except:
            pass

        with open(self.path_output+"lncRNA_GTF/lncRNA_selected.gtf", "w") as f:
            f.write(lncRNA_gtf)

        # Path
        path_lncRNA_selected_GTF = self.path_output + "lncRNA_GTF/lncRNA_selected.gtf"

        # Read files
        df_lncRNA_gtf = pd.read_table(path_lncRNA_selected_GTF, header=None)

        # Seperate lnc isoform id
        lnc_isoforms_id = []
        for index, row in df_lncRNA_gtf.iterrows():
            lnc_isoforms_id.append(row[8].split(";")[1].split(" ")[1].split('"')[1])
        lnc_isoforms_unique = set(lnc_isoforms_id)

        # Read lncRNA selected GTF
        lncIsoform_selected_gtf = []
        with open(path_lncRNA_selected_GTF, "r") as f:
            for l in f:
                lncIsoform_selected_gtf.append(l)

        # Seperate lnc isoform gtf
        for lncIso in lnc_isoforms_unique:

            try:
                os.makedirs(self.path_output + "lncRNA_GTF/")

            except:
                pass

            path_lncIso_block = self.path_output + "lncRNA_GTF/%s.gtf" % lncIso
            with open(path_lncIso_block, "w") as lncIso_block:
                for gtf in lncIsoform_selected_gtf:
                    if lncIso.strip() in gtf:
                        lncIso_block.write(gtf)


    def mRNA_GTF(self):

        # Path
        path_mRNA_gtf = self.path_root + "hg19_genes.gtf"
        path_selected_mRNA = self.path_output + "mRNA_selected_locus.csv"

        # Read mRNA GTF
        with open(path_mRNA_gtf, "r") as mRNA_gtf:
            mRNA_gtf_list = []
            for l in mRNA_gtf:
                mRNA_gtf_list.append(l)

        try:
            os.makedirs(self.path_output + "mRNA_GTF")
        except:
            pass

        # Read mRNA list
        mRNA_list = pd.read_csv(path_selected_mRNA, sep="\t")["gene_id"]

        # mRNA selection
        for mRNA in mRNA_list:
            print(mRNA)

            path_mRNA_anno = self.path_output + "mRNA_GTF/" + mRNA.strip() + "_mRNA.gtf"
            with open(path_mRNA_anno, "w") as mRNA_anno:
                for l in mRNA_gtf_list:
                    mRNA_id = '"'+ mRNA.strip() + '"'
                    if mRNA_id in l:
                        mRNA_anno.write(l)


    """
    This module need to be tested and fixed
    """
    def lncRNA_mRNA_GTF_assign(self):

        # Path
        path_lncRNA_mRNA = self.path_output + "lncRNA_mRNA.txt"
        path_Final = self.path_output + "Final_result/"


        lncRNA_mRNA = []
        with open(path_lncRNA_mRNA, "r") as f:
            for l in f:
                lncRNA_mRNA.append(l)

        path_lncIsoform_gtf = self.path_output + "lncRNA_GTF/"
        path_mRNA_gtf = self.path_output + "mRNA_GTF/"

        try:
            os.makedirs(path_Final)
        except:
            shutil.rmtree(path_Final)
            os.mkdir(path_Final)

        lncIsoformGTFs_list = os.listdir(path_lncIsoform_gtf)

        # Tranverse lncRNA_mRNA corresponding list
        for row in lncRNA_mRNA:
            lncRNA  = row.split("\t")[0]
            mRNAs   = row.strip().split("\t")[1:]

            # Tranverse from lncIsoforms
            for lncIsoGTF_file in lncIsoformGTFs_list:


                lncIso_id = lncIsoGTF_file.split(":")[0]

                if lncRNA == lncIso_id:
                    dir_lncIsoform = path_Final + lncIsoGTF_file.strip(".gtf") + "/"


                    try:
                        os.makedirs(dir_lncIsoform)
                        print(dir_lncIsoform)
                    except:
                        shutil.rmtree(dir_lncIsoform)
                        os.mkdir(dir_lncIsoform)

                    shutil.copy(path_lncIsoform_gtf+lncIsoGTF_file, dir_lncIsoform)

                    for mRNA in mRNAs:
                        for mRNA_GTF in os.listdir(path_mRNA_gtf):
                            if mRNA in mRNA_GTF:
                                shutil.copy(path_mRNA_gtf+mRNA_GTF, dir_lncIsoform)



if __name__ == "__main__":

    main = main()

    print("\nStart running ...")
    start_t = time.time()

    main.lncRNA_flankLocus()

    main.mRNA_locus()

    main.lncRNA_flank_mRNA_Match()

    main.lncRNA_mRNA_listSeperation()

    main.lncRNA_GTF()

    main.mRNA_GTF()

    main.lncRNA_mRNA_GTF_assign()

    total_t = time.time() - start_t

    print("\nTime consumed: %0.2f s" % total_t)