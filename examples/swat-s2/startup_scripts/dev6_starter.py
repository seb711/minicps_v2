import shlex
import subprocess


outputfile = open("./logs/dev6_logs.txt", "w")
subprocess.call(shlex.split('sudo python dev6.py'), stdout=outputfile)