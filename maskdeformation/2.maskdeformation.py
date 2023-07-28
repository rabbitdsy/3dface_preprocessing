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
    mi=min([lamda3,lamda2,lamda1])
    if lamda1==mi:
        lamda1=1-lamda3-lamda2
    if lamda2==mi:
        lamda2=1-lamda3-lamda1
    if lamda3==mi:
        lamda3=1-lamda1-lamda2
    return np.array([lamda1,lamda2,lamda3])

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
files=glob.glob(os.path.join("/data/dusiyuan/3Dface/GPA/",'*.csv'))
savepath="/data/dusiyuan/3Dface/GPA_EUR/"
maskeur=np.genfromtxt('/data/dusiyuan/3Dface/maskdeformation/eurmask.obj')
mask=np.genfromtxt('/data/dusiyuan/3Dface/maskdeformation/0000.obj')
mask_str=np.genfromtxt('/data/dusiyuan/3Dface/maskdeformation/0000.obj',dtype='<U32')
maskeur_str=np.genfromtxt('/data/dusiyuan/3Dface/maskdeformation/eurmask.obj',dtype='<U32')
faces=np.array(mask[7906:,1:],dtype=int)-1
lamda=np.genfromtxt('/data/dusiyuan/3Dface/maskdeformation/lamda.csv',delimiter=',')
index=np.array(lamda[:,0],dtype=int)
lamda=lamda[:,1:]
#%%
for f in files[0:len(files)]:
    points=np.genfromtxt(f,delimiter=',')+np.array([0,16,54])
    #points=np.array(points[0:7906,1:],dtype="float")
    cordinate=np.zeros((7160,3))
    for i in range(0,len(index)):
        #print(i)
        tri=points[faces[index[i]]]
        cordinate[i]=bar2car(tri,lamda[i]/sum(lamda[i]))
    maskeur_str[0:7160,1:]=cordinate
    mask_str[0:7906,1:]=points
    print(f)
    #np.savetxt(savepath+f.split('/')[-1].split('.')[0]+".obj",mask_str,delimiter=' ',fmt='%s')
    np.savetxt(savepath+f.split('/')[-1].split('.')[0]+"_eur.obj",maskeur_str,delimiter=' ',fmt='%s')
    np.savetxt(savepath+f.split('/')[-1].split('.')[0]+".csv",cordinate,delimiter=',',fmt='%s')

#%%
