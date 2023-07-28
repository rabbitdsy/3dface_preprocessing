#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests  
import json  
import numpy as np
import os
import sys
import glob
from utils import *

index=[137, 122, 160, 176, 208, 237, 261]
objFilePath=sys.argv[1]
landmarkPath=sys.argv[2]
savepath=sys.argv[3]
savename=savepath+objFilePath.split('\\')[-1][0:-4]

pointsraw,faceraw=readobjbellus(objFilePath)
landmark,f=readobjnormal(landmarkPath)
landmark3d=landmark[index,]

TT=transformation_from_points(landmark3d,modelb,False)
pointsnew=(np.matrix(pointsraw) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])
writeobj(savename,pointsnew,faceraw)


'''
points=np.array([
[-36.598541,29.493992,26.594152],
[-12.289736,30.017504,29.354811],
[27.987465,31.188320,28.003490],
[49.350960,29.957150,26.182228],
[5.873141,2.352704,76.778946],
[-19.598864,-42.782257,44.326981],
[30.839588,-42.369263,45.705215]])
index=[]
for p in points:
    temp=landmark-p
    temp=np.sum(temp**2,1)
    index.append(np.where(temp==min(temp))[0][0])
'''