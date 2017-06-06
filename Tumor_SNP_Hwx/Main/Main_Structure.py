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
                           |-- 2> Check Software
                           |
                           |-- 3> Check Database
                           |
                           |-- 4> Check Directory


--|3| getArgs.py |
                      |
                      |  |1|-- Check Preparation
                      |--|
                         |2|-- Main


--|4| qualityCtrl.py |


--|5| mapping.py |


--|4-1| gatk.py |


--|4-2| varscan2.py |


--|*| reportPack.py |



"""
