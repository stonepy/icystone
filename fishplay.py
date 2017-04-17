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


day    = total_time // (3600 * 24)
hour   = total_time // (3600) % 24
minute = total_time / 60 % 60
second = total_time % (60)


print("\n\n>>> Total time: |> %id %ih %im %.2fs <| (Total second(s): %.2fs)\n" % (day, hour, minute, second, total_time))