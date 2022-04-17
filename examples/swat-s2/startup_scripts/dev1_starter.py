import shlex
import subprocess

outputfile = open("./logs/dev1_logs.txt", "w")
subprocess.call(shlex.split('sudo python dev1.py'), stdout=outputfile)