"""

"""

"""
Pipline:

--|1| Main |
           |
           |           |-- 0> Check Exiting Result   |<<===| 'Checking.py'
           |-- Fuction |
           |           |-- 1> Run Function           |<<===| '<function_package>.py'
           |           |
           |           |-- 2> Summary Result in "Data_Analysis" Directory
           |           |
           |           |-- 3> Check Result           |<<===| 'Checking.py'
           |           |
           |           |-- 4> Copy Result to 'Report' Directory
           |
           |-- Report Html/PDF
           |
           |-- Pack and Compress


--|2| Check |
            |
            |  |-- 0> Get Argument          |<<===| 'get_args.py'
            |--|
               |-- 1> Check/Load Package    |<<===| 'checking.py'
               |
               |-- 2> Check Software        |<<===| 'Checking.py'
               |
               |-- 3> Check Database        |<<===| 'Checking.py'
               |
               |-- 4> Check Directory       |<<===| 'Checking.py'


--|M| ManageExecution |
                      |
                      |  |1|-- Check
                      |--|
                         |2|-- Main

"""





"""
Pacakge:

--|1| checking.py |
                  |
                  |           |-- 0> Check Exiting Result
                  |-- Fuction |
                  |           |-- 1> Run Function
                  |           |



--|2| setting.py |
                 |
                 |  |-- 0> Get Argument
                 |--|
                    |-- 1> Check/Load Package
                           |
                           |-- 2> Check Software: Path exits
                           |
                           |-- 3> Check Database: Path exits
                           |
                           |-- 4> Check Directory: Path exits


--|3| getArgs.py |
                 |
                 |  |1|-- Check
                 |--|
                    |2|-- Main


--|4| configProcess.py |


--|5| qualityCtrl.py |


--|6| mapping.py |


--|7-1| gatk.py |                                       |-- 1> mpileup
                |                       |-- 1> samtools |
                |  |-- 0> BAM_Processor |               |-- 2> chr_split
                |  |                    |
                |--|                    |             |-- 1> index
                   |                    |-- 2> picard |
                   |
                   |
                   |-- 1> UnifiedGenotyper
                   |
                   |-- 2> MuTect2
                   |
                   |-- 3> MuTect2


--|7-2| varscan2.py |
                    |
                    |  |-- 1> somatic
                    |--|


--|*| processManage.py |
                       |
                       |  |-- 1>


--|*| reportPack.py |


--|*| log.py |



"""
