##########################################################
# Author : Hwx                                           #
# Date   : 2016-9-30                                     #
# Purpose: KaKs ratio calculation, statistic and figure  #
##########################################################

# import package
import os
import matplotlib
matplotlib.use('Agg')

import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt


# # def a class
class KaKs_ratio:
    # Initialize the parameters including path and raw data
    def __init__(self):
		
	# # Work path
        self.path_work = os.getcwd() + "/"

        # # Input path list
        self.path_rawdata_input    = self.path_work + "allSNV.txt"
        print(self.path_rawdata_input)
        print("Start input file")
        # # Read data file
        self.data_rawdata_input    = pd.read_table(self.path_rawdata_input)
        print("Finished raw data input")

        # # Output path list
        self.path_clean_output     = self.path_work + "allSNV_clean.csv"
        self.path_genelist_output  = self.path_work + "allSNV_genelist.csv"
        self.path_snprate_output   = self.path_work + "allSNV_snprate.csv"
        self.path_result_output    = self.path_work + "allSNV_KaKs.csv"
        self.path_figure_output    = self.path_work + "Kaks_genestat.pdf"

    # # Clean the raw data, strip the useless information
    def data_clean(self):

        # # Cleanning raw data
        self.data_clean_1 = self.data_rawdata_input.ix[:,["SNV NO.",
                                                          "Gene",
                                                          "Function",
                                                          "Case mutation",
                                                          "Case(wild|mutation)"
                                                          ]]
        self.data_clean_2 = self.data_clean_1.dropna()
        self.data_clean = self.data_clean_2.sort_index(by='Gene')
        self.data_clean.to_csv(self.path_clean_output)
        print("Finished data clean")

    # # Extract gene list and calculate SNP rate
    def data_preparation(self):

        # # Extract the useful data and acquire the gene list
        try:
            self.data_clean
        except:
            self.data_clean = pd.read_csv(self.path_clean_output)

        self.data_input = self.data_clean.ix[:,["Gene","Function","Case mutation","Case(wild|mutation)"]]
        self.gene_list = self.data_input["Gene"].drop_duplicates()

        # # Extract the mutation information and calculate snp rate of each SNP site
        self.snp_ratio = []
        for wt_snp in self.data_input["Case(wild|mutation)"]:
            wt, snp = wt_snp.split("|")
            self.snp_ratio.append(int(snp)/(int(snp) + int(wt)))
            self.snp_ratio_set = pd.DataFrame(self.snp_ratio,columns=["snp_ratio"])

        self.gene_list.to_csv(self.path_genelist_output)
        self.data_snpratio = pd.concat([self.data_input,self.snp_ratio_set],axis=1)
        self.data_snpratio.to_csv(self.path_snprate_output)
        print("Finished data preparation")

    # # This is core which calcualtes the Ka/Ks ratio
    def calculate_KaKs(self):

        # Prepare Nan data set
        self.ka_ratio = []
        self.ks_ratio = []
        self.ka_count = []
        self.ks_count = []
        self.kaks_ratio_set = []
        self.kaks_count_set = []

        # Extract the gene set and calculate the KaKs rate
        try:
            self.gene_list
        except:
            self.gene_list = pd.read_csv(self.path_genelist_output)

        try:
            self.data_snpratio
        except:
            self.data_snpratio = pd.read_csv(self.path_snprate_output)

        for gene in self.gene_list:
            # Acquire the gene set
            self.gene_set = self.data_snpratio[self.data_snpratio['Gene']==gene]

            # Acquire the total of synonymous and non-synonymous snp rate
            self.sum_snpratio_syn,self.sum_snpratio_nonsyn = self.gene_set[self.gene_set['Function']=='synonymous SNV']['snp_ratio'].sum(),self.gene_set[self.gene_set['Function'] == 'nonsynonymous SNV']['snp_ratio'].sum()
            self.sum_snpcount_syn,self.sum_snpcount_nonsyn = self.gene_set[self.gene_set['Function'] == 'synonymous SNV']['Function'].count(),self.gene_set[self.gene_set['Function'] == 'nonsynonymous SNV']['Function'].count()

            # # This is the very core part: -<| Calculate of KaKs_ratio |>-

            # Calculate Ka/Ks considering the snp distribution in each group
            ka = self.sum_snpratio_nonsyn
            ks = self.sum_snpratio_syn
            self.ka_ratio.append(ka)
            self.ks_ratio.append(ks)
            # print(ka,ks)
            if self.sum_snpratio_syn == 0:
                ks = 0.01
            kaks_ratio = ka / ks
            self.kaks_ratio_set.append(kaks_ratio)

            # Calculate Ka/Ks considering the snp distribution in each group
            ka         = self.sum_snpcount_nonsyn
            ks         = self.sum_snpcount_syn
            if self.sum_snpratio_syn == 0:
                ks = 0.01
            kaks_count = ka / ks
            self.kaks_count_set.append(kaks_count)
        print("Finished calculation")

    # # Summary and output the result
    def result_summary(self):

        # Collect results
        self.result_set = {
            "Gene"       : self.gene_list,
            "Ka"         : self.ka_ratio,
            "Ks"         : self.ks_ratio,
            # "kaks_count" : self.kaks_count_set,
            "kaks_ratio" : self.kaks_ratio_set
        }
        self.result_set = pd.DataFrame(self.result_set)

        # Output the result
        self.result_set = self.result_set.dropna()
        self.result_set.to_csv(self.path_result_output)
        print("Finished summary")

		
    # # Plot the statistic result of Ka/Ks ratio and genes
    def plot_hist(self):

        # If the result file of KaKs is exist, time can be saved by skipping steps all above and plotting directly
        try:
            self.result_set
        except:
            self.result_set = pd.read_csv(self.path_result_output)
        self.kaks_ratio_set = self.result_set["kaks_ratio"]

        # Acquire x value for x axis
        value_xAxis = []
        for i in self.kaks_ratio_set:
            if i >= 5:
                value_xAxis.append(5)
            else:
                value_xAxis.append(i)
        value_xAxis = pd.Series(value_xAxis).dropna()

        # Set the x axis
        x_max = round((max(self.kaks_ratio_set) * 10 + 1), 0)
        if  x_max >= 5:
            x_max = 52
        bins = []
        for i in range(0, int(x_max), 2):
            bins.append(i * 0.1)

        # Set the hist bins
        hist, bins = np.histogram(value_xAxis, bins=bins)
        width = np.diff(bins)
        center = (bins[:-1] + bins[1:]) / 2

        # Set figure attribute
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.bar(center, hist, align='center', width=width, facecolor='green', edgecolor='white', alpha=0.5)

        # Set figure information
        font_title = {'family': 'serif',
                'color': 'black',
                'weight': 'normal',
                'size': 38,
                }
        font_label = {'family': 'serif',
                'color': 'darkred',
                'weight': 'normal',
                'size': 26,
                }
        ax.set_xticks(bins)
        ax.set_xlabel('Ka/Ks ratio', fontdict=font_label)
        ax.set_ylabel('Amount of specific Ka/Ks', fontdict=font_label)
        ax.set_title('Ka/Ks Pressure selection', fontdict=font_title)

        # Save the figure
        fig.savefig(self.path_figure_output)
        print("Finished plotting histogram")
        plt.show()


if __name__ == "__main__":

    kaks_ratio = KaKs_ratio()

    # kaks_ratio.data_clean()
    # kaks_ratio.data_preparation()
    # kaks_ratio.calculate_KaKs()
    # kaks_ratio.result_summary()
    kaks_ratio.plot_hist()


    print("Finished KaKs Process")
	
	
