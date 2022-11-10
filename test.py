import tkinter
import subprocess,shlex
args = shlex.split("mkdir ./abc")
proc = subprocess.call(args)
tkinter._test()