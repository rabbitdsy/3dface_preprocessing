# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:15:01 2023

@author: user
"""

import glob
import os

objFilePath="D:\\3Dface\\qingdao2\\obj\\"#sys.argv[1]
landmarkPath="D:\\3Dface\\qingdao2\\landmark\\"#sys.argv[2]
savepath="D:\\3Dface\\qingdao2\\step1\\"#sys.argv[3]

files=glob.glob(os.path.join(objFilePath,'*.obj'))
files.sort()
f=open('runcmd.txt','w')
for file in files:
    name=file.split("\\")[-1][0:-4]
    f.write("python step1.py "+objFilePath+name+".obj "+landmarkPath+name+'.obj '+ savepath+name+'\n')
    
f.close()




# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:15:01 2023

@author: user
"""

import glob
import os

objFilePath="D:\\3Dface\\qingdao2\\step3\\"#sys.argv[1]
savepath="D:\\3Dface\\qingdao2\\step4\\"#sys.argv[3]

files=glob.glob(os.path.join(objFilePath,'*.obj'))
files.sort()
f=open('D:\\3Dface\\qingdao2\\scripts\\runstep4.txt','w')
for file in files:
    name=file.split("\\")[-1][0:-4]
    f.write("python step4.py "+objFilePath+name+".obj "+ savepath+'\n')
    
f.close()