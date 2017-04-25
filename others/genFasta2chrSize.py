Description = """

- Information -------------------------------------------------------------------
 Name         : genFasta2chrSize
 Description  : Convert Genome_Fasta to Chromesome_Size
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-25
---------------------------------------------------------------------------------

"""

import sys


# Test parameters
iput_path = "GCF_000005845.2_ASM584v2_genomic.fna"
out_path  = "GCF_000005845.2_ASM584v2_genomic.size"

# Get arguments
args = sys.argv

# Check if user didn't provide valid path
try:
    iput_path = args[1]
    out_path  = args[2]

except IndexError:
    print(Description)
    print("[ Usage ]\n    python scriptName.py <fasta_PATH> <output_PATH>\n\n")


def main():

    with open(iput_path, "r") as fa:

        chrSize  = open(out_path, "w")    # Chromesome size file
        chrLen = None                     # Length of each chromesome

        for l in fa:
            if l.startswith(">"):

                # Skip the first line, and record last calculated aggregation
                if chrLen != None:
                    chrSize.write("%s\t%s\n" % (chrName, str(chrLen)))

                chrLen = 0              # Empty last chromesome size
                chrName = l.strip()
                continue

            chrLen += len(l)            # Calculate the size of chromesome

        # Record last size of chromesome
        if chrLen != 0:
            chrSize.write("%s\t%s\n" % (chrName, str(chrLen)))

        chrSize.close()



if __name__ == "__main__":
    main()