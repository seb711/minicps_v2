import shlex
import subprocess

outputfile = open("./logs/phy_logs.txt", "w")
subprocess.call(shlex.split('sudo python physical_process.py'), stdout=outputfile)