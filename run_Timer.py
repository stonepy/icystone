Description = """

_ Information ____________________________________________________________________
 Name         : run_Timer
 Description  : Time for script running
 Author       : Hwx
 Version      : V2
 Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-17
___________________________________________________________________________________


"""



import subprocess
import sys
import time


args = sys.argv
cmd = " ".join(args[1:])

print(time.ctime())
print("\n>>> Executing CMD: %s\n\n" % cmd)

start_time = time.time()

try:
    subprocess.call(cmd, shell=True)
except Exception as e:
    print(e)

total_time = time.time() - start_time

# Convert second to minute,hour and day.
day    = total_time // (3600 * 24)
hour   = total_time // (3600) % 24
minute = total_time / 60 % 60
second = total_time % (60)


print("\n\n>>> Total time: |> %id %ih %im %.2fs <| (Total second(s): %.2fs)\n" % (day, hour, minute, second, total_time))