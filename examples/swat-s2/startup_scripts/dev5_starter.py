import shlex
import subprocess


outputfile = open("./logs/dev5_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./devices/dev5.py'), stdout=outputfile)
