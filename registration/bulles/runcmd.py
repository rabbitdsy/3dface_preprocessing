#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import glob
cmd=open('cmd.sh','w')
cmd.write('''#!/bin/bash
export OMP_NUM_THREADS=1
printf step1
''')

if len(sys.argv)!=4:
    print(len(sys.argv))
    print('''\n***************************\n***************************\nThe script require 3 parameters, see example:
    python runcmd.py objFilePath Parallel_count capture_device(3dmd/vectra)\n\n***************************\n***************************\n''')
    quit()

objFilePath=sys.argv[1]
count=int(sys.argv[2])
device=str(sys.argv[3])
if os.path.exists("../step1")==False:
    os.mkdir("../step1")
if os.path.exists("../step2")==False:
    os.mkdir("../step2")

if os.path.exists("../step3")==False:
    os.mkdir("../step3")

if os.path.exists("../step4")==False:
    os.mkdir("../step4")

#%% STEP 1
rawobj=glob.glob(os.path.join(objFilePath,'*.obj'))
rawobj.sort()
c=0
for obj in rawobj:
    c=c+1
    cmd.write('python step1.py '+obj+' ../step1/ '+device)
    if c%count==0:
        cmd.write("\nwait\n")
    else:
        cmd.write(' & \n')

cmd.write('''wait\nprintf step2.1\n''')

#%% STEP 2
c=0
for obj in rawobj:
    c=c+1
    obj=obj.split('/')[-1]
    cmd.write('python step2.py ../step1/'+obj+' ../step2/\n')

cmd.write('wait\nprintf step2.2\n')

#%% STEP 2.2
c=0
for obj in rawobj:
    c=c+1
    obj=obj.split('/')[-1]
    cmd.write('python step2.2.py ../step1/'+obj+' ../step2/')
    if c%count==0:
        cmd.write("\nwait\n")
    else:
        cmd.write(' & \n')

cmd.write('wait\nprintf step3\n')

#%% STEP 3
cmd.write('''matlab -nosplash -nodesktop -r "step3;quit()"\n''')
cmd.write('wait\nprintf step4\n')

#%% STEP 4
c=0
for obj in rawobj:
    c=c+1
    obj=obj.split('/')[-1]
    cmd.write('python step4.py ../step3/'+obj+' ../step4/')
    if c%count==0:
        cmd.write("\nwait\n")
    else:
        cmd.write(' & \n')

cmd.write('wait\n')








