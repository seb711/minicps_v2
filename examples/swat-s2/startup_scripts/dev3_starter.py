import shlex
import subprocess

outputfile = open("./logs/dev3_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./devices/dev3.py'), stdout=outputfile)