import shlex
import subprocess

outputfile = open("./logs/dev2_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./devices/dev2.py'), stdout=outputfile)