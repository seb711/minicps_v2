import shlex
import subprocess

outputfile = open("./logs/plc1_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./plcs/plc1.py'), stdout=outputfile)