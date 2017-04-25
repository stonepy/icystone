Description = """

- Information --------------------------------------------------------------------
 Name         : Script_Framework
 Description  : Build new project with it, simple edition
 Author       : Hwx
 Version      : V2
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-15
-----------------------------------------------------------------------------------

"""


import sys
import os

# Test parameters
path = None

# Get arguments
args = sys.argv

# Check if user didn't provide valid path
try:
    path = args[1]

except IndexError as e:
    print("\n>>> Error :\n    %s\n" % e)
    print("\n===============================================\n[ Usage ]\n    python scriptName.py <args>\n===============================================\n")

    path = input("\nYou can provide availabe arg here, please input the arg : \n")

    if not os.path.exists(path):
        print("\n>>> Error :\n    Sorry, you didn't provide valid path\n")
        exit()


def main():

    def __init__():
        pass



if __name__ == "__main__":

    main()
