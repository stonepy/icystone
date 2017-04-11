"""

Name        : get_SampleNames
Description : Get all names of samples and list in a line seperated by comma
Author      : Hwx
Version     : V1
Date        : 2017-02-06

"""



import os
import sys


# Get arguments
args = sys.argv

# Check if user didn't provide valid path
try:
    path_rawdata = args[1]
except IndexError as e:

    print("\n===============================================\n[ Usage ]\n    python get_SampleNames.py <rad_data_path>\n===============================================\n")

    path_rawdata = raw_input("\nYou can provide availabe raw_data_path here, please input the path : \n")

    if not os.path.exists(path_rawdata):
        print("\n>>> Error :\n    Sorry, you didn't provide valid raw_data path\n")
        exit()



def get_SampleNames(path_input):
    # Check if the directory assigned by user is exist
    while not os.path.exists(path_input):
        path_input = input(
            ">>> Error : \n    Raw data directory can't be found, please enter the right path : ")

    # For store sample names and suffixs
    names = []
    suffixs = []
    uniq_names = []
    uniq_suffixs = []

    # When there is no qualified data go on collecting
    while len(names) == 0:

        # List all samples in rawData directory
        files = os.listdir(path_input)

        # Abstract sample name
        for f in files:

            # Exclude other files than ".fastq" and ".fastq.gz"
            if f.endswith(".fastq.gz") or f.endswith(".fastq") or f.endswith(".fasta") or f.endswith(
                    ".fq") or f.endswith(".fa"):

                try:

                    # Split out names and suffixs
                    name = f.split("_")[0]
                    suffix = f.split(".")[-1]

                    # Collect names and suffixs
                    names.append(name)
                    suffixs.append(suffix)

                # If there something goes wrong, warn user
                except Exception as e:
                    print(e)

        # Remove duplicated names
        uniq_names = list(set(names))
        uniq_suffix = list(set(suffixs))

        # Check if the type of sample files is unique
        if len(uniq_suffix) > 1:
            print(
                ">>> Warning :\n    There are more than 1 type of file among the sample data : %s\n    Please make sure there is only one type ..." % uniq_suffix)

            # If there are more than one type , then exit
            exit()

        # Check if there is enough sample data or if sample data is single-end
        elif len(suffixs) % 2 != 0:
            print(">>> Warning :\n    These samples are 'Single-End' or lack of sample.\n")

        # Check if sample data is in the directory that user assigned
        elif len(uniq_names) == 0:
            path_input = input(
                ">>> Error :\n    Sample data can not be found in directory \" %s \", please input a directory that store sample data : " % path_input)
            print()

        # If all things goes well, then tell user this :
        else:
            print("\n|- These samples are 'Paired-End'\n")

    # Show sample names
    print(
        "|- Samples will be analysis :\n    Sample : %s \n    File Types : %s \n" % (",".join(sorted(uniq_names)), uniq_suffix))

    # Return the names and suffixs
    return uniq_names, uniq_suffix


if __name__ == "__main__":
    get_SampleNames(path_rawdata)
