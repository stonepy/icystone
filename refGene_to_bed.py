"""
- Information --------------------------------------------------------------------
 Name         : refGene_to_bed
 Description  : Transform '*_refGene.txt' to '*.bed', '*' stands for species, specific for SNP pipline
 Formulation  : None
 Author       : Hwx
 Version      : V3
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Windows10 Home CN, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-10
-----------------------------------------------------------------------------------
"""

import time
import sys
import re


# Test path
path_refGene   = "mm10_refGene_old.txt"
path_BedOutput = "mm10_new.bed"

# Parse arguments
args = sys.argv
try:
    path_refGene   = args[1]
    path_BedOutput = args[2]

except:
    print("""
    Usage:
        python refGene_to_bed.py <refGene_input> <BEDoutput_output>
    """)
    exit()

# Start timing
start_t = time.time()

# Import pandas here for faster launching
import pandas as pd

# Get name of IO file names
inputFile = re.split("/|\|", path_refGene)[-1]
outputFile = re.split("/|\|", path_BedOutput)[-1]

print("\nReading %s ......" % inputFile)

# Read '*_refGene.txt' as DataFrame
df_refGene = pd.read_table(path_refGene, header=None)

# Seperate information and output to '*.bed'
with open(path_BedOutput, "w") as bed:
    # Sort by chromosome
    df_refGene = df_refGene.sort_values(by=2, ascending=True)

    print("Converting %s into %s ......" % (inputFile, outputFile))

    # Obtain information
    for index, row in df_refGene.iterrows():
        iso   = row[1]                          # Isoform name
        chr   = row[2].strip("chr")             # Chromosome, only need number
        ori   = row[3]                          # Orientation
        start = row[9].split(",")[:-1]          # Start site
        end   = row[10].split(",")[:-1]         # End site

        # Output the treated items
        n = 0               # Count of isoform
        for coord in zip(start, end):

            n += 1
            iso_n = iso + "." + str(n)      # Use id of isoform and number to identify name, must convert number to string
            l = "\t".join([str(chr), str(coord[0]), str(coord[1]), str(ori), iso_n]) + "\n"     # Merge all items into a line
            bed.write(l)

print("Finish convertion.\n")

# Stop timing
total_t = time.time() - start_t
print("Time concumed: %0.2fs\n" % total_t)
