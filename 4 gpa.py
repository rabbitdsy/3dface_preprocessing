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

savepath="../step3/"
objs=glob.glob(os.path.join("../step2/",'*.obj'))


for objFilePath in objs:
    savename=savepath+objFilePath.split('\\')[-1][0:-4]
    pointsraw,faceraw=readobjnormal(objFilePath)
    template=np.genfromtxt('Template.txt')
    TT=transformation_from_points(pointsraw,template,True)
    pointsnew=(np.matrix(pointsraw) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])
    TT=transformation_from_points(pointsnew,template,False)
    pointsnew=(np.matrix(pointsnew) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])
    np.savetxt(savename+'.csv',pointsnew,delimiter=',')
    writeobj(savename,pointsnew,faceraw)




# In[2]



# import cv2  
# import requests  
# import json  
# import numpy as np
# import os
# import sys
# import glob
# from utils import *

# pointsraw=np.genfromtxt('ADNP_all_avg.csv',delimiter=',')
# template=np.genfromtxt('all_avg.csv',delimiter=',')
# TT=transformation_from_points(pointsraw,template,True)
# pointsnew=(np.matrix(pointsraw) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])
# TT=transformation_from_points(pointsnew,template,False)
# pointsnew=(np.matrix(pointsnew) * np.matrix(TT[0:3,0:3]).T + TT[0:3,3])


# np.savetxt('ADNP_all_avg2'+'.csv',pointsnew,delimiter=',',fmt='%s')


#writeobj(savename,pointsnew,faceraw)



