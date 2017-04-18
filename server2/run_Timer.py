import subprocess
import sys
import time
import os

args = sys.argv
cmd = " ".join(args[1:])

print("\n>>> Executing command: %s\n\n" % cmd)

start_time = time.time()

try:
    os.system(cmd)
except Exception as e:
    print(e)

finish_time = time.time()
total_time = finish_time - start_time

print("\n\n>>> Total time: %.5f s\n" % total_time)
