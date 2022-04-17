import shlex
import subprocess

outputfile = open("./logs/dev4_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./devices/dev4.py'), stdout=outputfile)