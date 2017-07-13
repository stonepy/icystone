"""
    Download database from 'Cosmic Drug Sensitivity' FTP, Demo
"""

import urllib.request
import time
import re
from subprocess import call

address = "ftp://ftp.sanger.ac.uk/pub4/cancerrxgene/releases/release-6.0/"

with urllib.request.urlopen(address) as response:

    for l in response:
        l = l.strip()
        filename = re.split("\t| |'", str(l))[-1]
        cmd = "wget %s%s &" % (address, filename)
        print(filename)
        call(cmd, shell=True)
        time.sleep(2)
