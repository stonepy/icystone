import subprocess
import sys
import time


args = sys.argv
cmd = " ".join(args[1:])

print("\n>>> Executing CMD: %s\n\n" % cmd)

start_time = time.time()

try:
    subprocess.call(cmd, shell=True)
except Exception as e:
    print(e)


total_time = time.time() - start_time


d = total_time // (3600 * 24)
h = total_time // (3600) % 24

m = total_time % (3600)

s = total_time % (60)


print("\n\n>>> Total time: %.5f s\n" % total_time)
