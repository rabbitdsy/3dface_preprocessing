# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:23:37 2022

@author: user
"""


import sys
import os
from joblib import Parallel, delayed
fileCmd=sys.argv[1]
ncore=sys.argv[2]
f=open(fileCmd)
check_cmd=[]
for line in f:
    line=line.rstrip()
    check_cmd.append(line)
    print(line)
f.close()
Parallel(n_jobs=int(ncore))(delayed(os.system)(command) for command in check_cmd)

