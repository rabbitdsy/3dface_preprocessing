# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:02:24 2019

@author: DSY
"""

#加载所需包
from matplotlib.path import Path
import pandas as pd
import numpy as np
import glob
import os
from math import *
import sys


start=sys.argv[1]
end=sys.argv[2]
start=int(start)
end=int(end)


#定义各种函数
#求三边长
def side_len(cordinate):
    c=np.sqrt(sum((cordinate[0]-cordinate[1])**2))
    b=np.sqrt(sum((cordinate[0]-cordinate[2])**2))
    a=np.sqrt(sum((cordinate[1]-cordinate[2])**2))
    #print(np.array([a,b,c]))
    return np.array([a,b,c])

#海伦公式计算三角形面积
def area(abc):
    p=sum(abc)/2.0
    mianji=np.sqrt(p*(p-abc[0])*(p-abc[1])*(p-abc[2]))
    #print(mianji)
    return mianji

#用点到各顶点连成的三角形面积和判断点是否在三角形内部
def inside(triangle,points):
    tri_area=area(side_len(triangle))
    area1=area(side_len(np.vstack((triangle[0],triangle[1],points))))
    area2=area(side_len(np.vstack((triangle[1],triangle[2],points))))
    area3=area(side_len(np.vstack((triangle[0],triangle[2],points))))
    #print(area3+area2+area1-tri_area)
    return np.round(area3+area2+area1-tri_area,5)

#笛卡尔坐标系转换成重心坐标系，求lamda值。因为python的有效位数问题，所以把最小那个用1-lam1-lam2，会准确一些。
def barcentric(triangle,points):
    ABC=area(side_len(triangle))
    PAB=area(side_len(np.vstack((triangle[0],triangle[1],points))))
    PBC=area(side_len(np.vstack((triangle[1],triangle[2],points))))
    PAC=area(side_len(np.vstack((triangle[0],triangle[2],points))))
    #print(PAB,PBC,PAC)
    lamda3=PBC/ABC
    lamda2=PAC/ABC
    lamda1=PAB/ABC
    #mi=min([lamda3,lamda2,lamda1])
    #if lamda1==mi:
    #    lamda1=1-lamda3-lamda2
    #if lamda2==mi:
    #    lamda2=1-lamda3-lamda1
    #if lamda3==mi:
    #    lamda3=1-lamda1-lamda2
    return np.array([lamda1,lamda2,lamda3,lamda1+lamda2+lamda3])

#重心坐标系转换成笛卡尔坐标系。
def bar2car(triangle,lamda):
    A=triangle[0]
    B=triangle[1]
    C=triangle[2]
    #AB=triangle[1]-triangle[0]
    #CA=triangle[2]-triangle[0]
    #BC=triangle[2]-triangle[1]
    return lamda[2]*A+lamda[1]*B+lamda[0]*C   

#读取pp文件
def readpp(filepath):
    file=open(filepath,"r")
    points=file.read()
    points=str(points).split("\n") 
    points=points[8:-2]
    result=np.zeros((len(points),4),dtype="<U32")
    i=0
    for point in points:
        point_temp=point.split(" ")
        point_temp.sort()
        point_temp=point_temp[3:]
        j=0
        for cor in point_temp:
            result[i][j]=cor.split("\"")[1]
            j+=1
        i+=1
    landmarks=np.array(result[:,1:],dtype='float')   #坐标点信息
    names=np.array(result[:,0])  #各点名称
    return landmarks,names

def writepp(filepath,pt,names):
    f = open(filepath, 'w')
    f.write('<!DOCTYPE PickedPoints>\n<PickedPoints>\n <DocumentData>\n  <DateTime date="2019-04-03" time="16:59:22"/>\n  <User name="DSY"/>\n  <DataFileName name=" rTL0004.csv .obj"/>\n  <templateName name=".pickPointsTemplate.pptpl"/>\n </DocumentData>\n')
    for i in range(0,len(pt)):
        f.write(" <point z=\"")
        f.write(str(pt[i][2]))
        f.write("\" x=\"")
        f.write(str(pt[i][0]))
        f.write("\" y=\"")
        f.write(str(pt[i][1]))
        f.write("\" active=\"1\" name=\"")
        f.write(names[i])
        f.write("\"/>\n")
        i=i+1
    f.write('</PickedPoints>\n')
    f.close()
#%%
#加载模板脸。然后用三个lamda把对应的点从重心系转回笛卡尔坐标系。
chang=end-start

mask=np.genfromtxt('/picb/dermatogenomics/dusiyuan/3D/traditional/segnew/eur/0000.obj',dtype='U32')
points_m=np.array(mask[0:7906,1:],dtype="float")
points_m=points_m+np.array([0,16,54])
faces=np.array(mask[7906:,1:],dtype=int)-1
points_m_xy=points_m[:,0:2]
#%% 读取.pp文件中的点坐标。
#我这里总共标定了19个特征点。具体可以用meshlab加载.pp文件看。
landmarks=np.genfromtxt('/picb/dermatogenomics/dusiyuan/3D/traditional/segnew/eur/templatemap.txt',delimiter='\t')
landmarks_xy=landmarks[:,0:2]
#%% 寻找点所在的三角形
#读取obj文件，前7906行是点的信息，后15598行是面的信息。面对应坐标点你应该理解的吧...不理解去网上查一下obj文件的格式说明或者来问我都行。
triangles=np.zeros(7160)
#遍历查找每个点在哪个面上。找到之后把面index保存到triangles里面。
for i in range(start,end):
    b=[]
    for j in range(0,len(faces)):
        tri=points_m[faces[j]]
        b.append(inside(tri,landmarks[i]))
    index=np.where(b==min(b))
    #print(i,names[i],faces[index],min(b))
    triangles[i]=int(index[0])
    print(min(b))

#各点所对应面的index保存在triangles里
        
#%%
#然后求lamda，把笛卡尔坐标转换成重心系。
lamdal=np.zeros((7160,4))
for i in range(start,end):
    ABC=points_m_xy[faces[int(triangles[i])]]
    pt=landmarks_xy[i]
    lamda_temp=barcentric(ABC,pt)
    lamdal[i,]=lamda_temp
#各点所对应的lamda保存的在lamdal里
lamdal=np.array(lamdal)[:,0:3]
#%%
face_lamda=np.vstack((np.array(triangles),np.array(lamdal).T)).T
np.savetxt("/picb/dermatogenomics/dusiyuan/3D/traditional/segnew/eur/lamdal/"+str(start)+"_"+str(end-1)+'lamdadsyval2.csv',face_lamda,delimiter=',')