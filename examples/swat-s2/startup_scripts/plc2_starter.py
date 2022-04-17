import shlex
import subprocess

outputfile = open("./logs/plc2_logs.txt", "w")
subprocess.call(shlex.split('sudo python ./plcs/plc2.py'), stdout=outputfile)