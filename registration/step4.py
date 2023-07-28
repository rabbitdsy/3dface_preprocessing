#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2  
import requests  
import json  
import numpy as np
import os
import sys
import glob
from utils import *


objFilePath=sys.argv[1]
savepath=sys.argv[2]
savename=savepath+objFilePath.split('\\')[-1][0:-4]
print(savename)
if os.path.exists(objFilePath)==False:
    err=open(savepath+'errorlist.txt','a')
    err.write(objFilePath+'\n')
    err.close()

pointsraw,faceraw=readobjnormal(objFilePath)
template=np.genfromtxt('Template.txt')
TT=transformation_from_points(pointsraw,template,False)
pointsnew=(np.matrix(pointsraw) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])
np.savetxt(savename+'.csv',pointsnew,delimiter=',')
writeobj(savename,pointsnew,faceraw)
