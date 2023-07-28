
import os
import sys
import glob
cmd=open('wrl2obj_cmd.sh','w')
cmd.write('''#!/bin/bash
export OMP_NUM_THREADS=1
''')

print('''\n***************************\n***************************\nThe script should be excuted in file folder contains wrl format.\n***************************\n***************************\n''')
c=0
count=30
files=glob.glob('*.wrl')
for obj in files:
    c=c+1
    cmd.write('python wrl2obj.py '+obj)
    if c%count==0:
        cmd.write("\nwait\n")
    else:
        cmd.write(' & \n')


