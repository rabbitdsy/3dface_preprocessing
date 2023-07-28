# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 11:05:41 2021

@author: DSY
"""


import cv2  
import requests  
import json  
import numpy as np
import os
import sys
import glob

#%% read obj

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0/gamma
    table = []
    for i in range(256):
        table.append(((i / 255.0) ** invGamma) * 255)
    table = np.array(table).astype("uint8")
    return cv2.LUT(image, table)


def readobj3dmd(objFilePath,needpca=False):
    with open(objFilePath) as file:
        points = []
        texture = []
        faceraw = []
        facetraw = []
        while 1:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "v":
                points.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "vt":
                texture.append((float(strs[1]), float(strs[2])))
            if strs[0] == "f":
                faceraw.append((strs[1].split("/")[0],strs[2].split("/")[0],strs[3].split("/")[0]))
                facetraw.append((strs[1].split("/")[1],strs[2].split("/")[1],strs[3].split("/")[1]))
        
        points=np.array(points)
                
    if needpca==True:
        points = pca(points)
        points[:,0]=points[:,0]-min(points[:,0])
        points[:,1]=points[:,1]-min(points[:,1])
        points[:,2]=points[:,2]-min(points[:,2])
        
    if needpca==False:
        points[:,0]=points[:,0]-min(points[:,0])
        points[:,1]=points[:,1]-min(points[:,1])
        points[:,2]=points[:,2]-min(points[:,2])
        
    textureraw = np.array(texture)
    
    
    faceraw=np.array(faceraw,dtype=int)-1
    facetraw=np.array(facetraw,dtype=int)-1
    
    face=np.ravel(faceraw)
    facet=np.ravel(facetraw)
    a=np.vstack((face,facet)).T
    a=np.array(a)
    a=duplicate_removal(a)
    b=[a[0,:]]
    for i in range(1,len(a)):
        if(a[i,0]!=a[i-1,0]):
            b.append(a[i,:])
    pointtoface=np.array(b)
    texture=np.zeros((points.shape[0],2))
    texture[pointtoface[:,0],:]=textureraw[pointtoface[:,1] ,]   
    img = cv2.imread(objFilePath[0:len(objFilePath)-3]+'bmp',)
    img = cv2.flip(img,0)
    texture[:,0]=texture[:,0]*img.shape[1]-1
    texture[:,1]=texture[:,1]*img.shape[0]-1
    texture=np.array(texture,dtype=int)
    texturecolor=[]
    for i in range(0,texture.shape[0]):
        texturecolor.append(img[texture[i,1],texture[i,0],:])
    texturecolor=np.array(texturecolor)
    return points,faceraw,texturecolor

def readobjvectra(objFilePath,needpca=False):
    with open(objFilePath) as file:
        points = []
        texture = []
        faceraw = []
        facetraw = []
        mtl=[]
        while 1:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0]=="usemtl":
                mt=(strs[1]).split('material')[1][0]
            if strs[0] == "v":
                points.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "vt":
                texture.append((float(strs[1]), float(strs[2])))
            if strs[0] == "f":
                mtl.append((mt,mt,mt))
                faceraw.append((strs[1].split("/")[0],strs[2].split("/")[0],strs[3].split("/")[0]))
                facetraw.append((strs[1].split("/")[1],strs[2].split("/")[1],strs[3].split("/")[1]))
    points = np.array(points)
    if needpca==True:
        points = pca(np.array(points))
    else:
        points[:,0]=points[:,0]-min(points[:,0])
        points[:,1]=points[:,1]-min(points[:,1])
        points[:,2]=points[:,2]-min(points[:,2])
    textureraw = np.array(texture)
    faceraw=np.array(faceraw,dtype=int)-1
    facetraw=np.array(facetraw)
    mtl=np.ravel(np.array(mtl,dtype=int)[np.where(facetraw[:,0]!=''),])
    face=np.ravel(faceraw[np.where(facetraw[:,0]!=''),])
    facet=np.ravel(np.array(facetraw[np.where(facetraw[:,0]!=''),],dtype=int))-1
    a=np.vstack((face,facet,mtl)).T
    a=np.array(a)
    a=duplicate_removal(a)
    b=[a[0,:]]
    for i in range(1,len(a)):
        if(a[i,0]!=a[i-1,0]):
            b.append(a[i,:])
    pointtoface=np.array(b)
    texture=np.ones((points.shape[0],2))
    texture[pointtoface[:,0],:]=textureraw[pointtoface[:,1],:]
    usemtl=np.ones((points.shape[0],1))
    usemtl[pointtoface[:,0],0]=pointtoface[:,2].T#-1
    texture=np.hstack((texture,usemtl))
    imgs=[[],[],[],[],[]]
    for i in [0,1,2,3,4]:
        if os.path.exists(objFilePath[0:len(objFilePath)-4]+str(i)+'.png'):
            img = cv2.imread(objFilePath[0:len(objFilePath)-4]+str(i)+'.png')
            img=cv2.flip(img,0)
            imgs[i]=(img)
        if os.path.exists(objFilePath[0:len(objFilePath)-4]+str(i)+'.jpg'):
            img = cv2.imread(objFilePath[0:len(objFilePath)-4]+str(i)+'.jpg')
            img=cv2.flip(img,0)
            imgs[i]=(img)
    texturecolor=[]
    for i in range(0,texture.shape[0]):
        img=imgs[int(texture[i,2])]
        texturecolor.append(img[int(texture[i,1]*img.shape[0]-1),int(texture[i,0]*img.shape[1]-1),:])
    texturecolor=np.array(texturecolor)
    
    return points,faceraw,texturecolor


def readobjbellus(objFilePath,needpca=False):
    with open(objFilePath) as file:
        points = []
        texture = []
        faceraw = []
        #facetraw = []
        while 1:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "v":
                points.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "vt":
                texture.append((float(strs[1]), float(strs[2])))
            if strs[0] == "f":
                faceraw.append((strs[1].split("/")[0],strs[2].split("/")[0],strs[3].split("/")[0]))
                #facetraw.append((strs[1].split("/")[1],strs[2].split("/")[1],strs[3].split("/")[1]))
        
        points=np.array(points)
                
    if needpca==True:
        points = pca(points)
        #points[:,0]=points[:,0]-min(points[:,0])
        #points[:,1]=points[:,1]-min(points[:,1])
        #points[:,2]=points[:,2]-min(points[:,2])
        
    if needpca==False:
        points=points
        
    
    
    faceraw=np.array(faceraw,dtype=int)-1
    #facetraw=np.array(facetraw,dtype=int)-1
    
    face=np.ravel(faceraw)
    #facet=np.ravel(facetraw)
    #a=np.vstack((face,facet)).T
    #a=np.array(a)
    #a=duplicate_removal(a)
    #b=[a[0,:]]
    #for i in range(1,len(a)):
    #    if(a[i,0]!=a[i-1,0]):
    #        b.append(a[i,:])
    #pointtoface=np.array(b)
    #texture=np.zeros((points.shape[0],2))
    #texture[pointtoface[:,0],:]=textureraw[pointtoface[:,1] ,]   
    #img = cv2.imread(objFilePath[0:len(objFilePath)-3]+'bmp',)
    #img = cv2.flip(img,0)
    #texture[:,0]=texture[:,0]*img.shape[1]-1
    #texture[:,1]=texture[:,1]*img.shape[0]-1
    #texture=np.array(texture,dtype=int)
    #texturecolor=[]
    #for i in range(0,texture.shape[0]):
    #    texturecolor.append(img[texture[i,1],texture[i,0],:])
    #texturecolor=np.array(texturecolor)
    return points,faceraw#,texturecolor

#%% pca
def pca(points):
    D,V=(np.linalg.eig(np.cov(np.matrix(points).T)))
    V=V[:,np.argsort(-D)]
    V=V[:,[1,0,2]]

    if V[0,0]<0:
        V[:,0]=-V[:,0]

    if V[1,1]<0:
        V[:,1]=-V[:,1]

    if V[2,2]<0:
        V[:,2]=-V[:,2]

    points=np.dot(points,V)
    points[:,0]=points[:,0]-min(points[:,0])
    points[:,1]=points[:,1]-min(points[:,1])
    points[:,2]=points[:,2]-min(points[:,2])
    return(points)

#%% gpa

def CentroidSize(points):
    points=np.array(points)
    centroid=np.mean(points,0)
    Differences = centroid-points;
    Distances = np.sqrt(np.sum(Differences**2,1));
    out = np.sqrt(np.sum(Distances**2)/len(Distances));
    print(out)
    return(out)




def transformation_from_points(points1, points2, isscale):
    """
    Return an affine transformation [s * R | T] such that:
        sum ||s*R*p1,i + T - p2,i||^2
    is minimized.
    """
    # Solve the procrustes problem by subtracting centroids, scaling by the
    # standard deviation, and then using the SVD to calculate the rotation. See
    # the following for more details:
    #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem
 
    points1 = np.matrix(points1.astype(np.float64))
    points2 = np.matrix(points2.astype(np.float64))
 
    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2
 
    #s1=np.mean(np.sqrt(np.sum(np.square(points1),1)))
    #s2=np.mean(np.sqrt(np.sum(np.square(points2),1)))
    s1=CentroidSize(points1)
    s2=CentroidSize(points2)
    points1 /= s1
    points2 /= s2
    scale=s2/s1


    U, S, Vt = np.linalg.svd(points1.T * points2)
 
    # The R we seek is in fact the transpose of the one given by U * Vt. This
    # is because the above formulation assumes the matrix goes on the right
    # (with row vectors) where as our solution requires the matrix to be on the
    # left (with column vectors).
    R = (U * Vt).T
    
    if(isscale==False):
        scale=1
    
    
    transform=R
    Ta=np.eye(4)
    Ta[0:3,3]=c2
    Tb=np.eye(4)
    Tb[0:3,3]=-c1
    R=np.eye(4)
    R[0:3,0:3]=transform
    Tout=np.dot(np.dot(Ta,R),Tb)
    print(Tout)
    Tout[0:3,0:3]=(U * Vt).T*scale

    return Tout

#%% utils

def duplicate_removal(xy):
  if xy.shape[0] < 2:
    return xy
  _tmp = (xy*4000).astype('i4')          # 转换成 i4 处理
  _tmp = _tmp[:,0] + _tmp[:,1]*1j         # 转换成复数处理 
  keep = np.unique(_tmp, return_index=True)[1]  # 去重 得到索引                  
  return xy[keep]                 # 得到数据并返回


def project(points,texturecolor):
    points=np.array(points,dtype=int)
    texturecolor=np.array(texturecolor,dtype='uint8')
    imgrgb=np.zeros((max(points[:,1])+10,max(points[:,0])+10,3),dtype='uint8')
    imgrange=np.zeros((max(points[:,1])+10,max(points[:,0])+10),dtype=int)
    for i in range(0,points.shape[0]):
        if points[i,2]>imgrange[points[i,1],points[i,0]]:
            imgrgb[points[i,1],points[i,0],:]=texturecolor[i,:]
            imgrange[points[i,1],points[i,0]]=points[i,2]
    imgrgb=cv2.medianBlur(np.array(imgrgb,dtype='uint8'),5)
    imgrgb=cv2.flip(imgrgb,0)
    #imgrange=cv2.medianBlur(np.array(imgrange,dtype='uint8'),3)
    #imgrange=cv2.flip(imgrange,0)
    return imgrgb,imgrange


def landmark3ds(landmark,pointsraw):
    landmark3d=[]
    for i in range(0,len(landmark)):
        temp=pointsraw[:,[0,1]]-landmark[i,]
        temp=np.sum(temp**2,1)
        landmark3d.append(pointsraw[np.where(temp==min(temp))[0][0],])
    landmark3d=np.array(landmark3d)
    return(landmark3d)

def writeobj(path,points,face):
    obj=open(path+'.obj','w')
    points=np.array(points)
    for v in points:
        obj.write('v '+str(round(v[0],3))+' '+str(round(v[1],3))+' '+str(round(v[2],3))+'\n')
    for f in face:
        obj.write('f '+str(f[0]+1)+' '+str(f[1]+1)+' '+str(f[2]+1)+'\n')
    obj.close()

def facepp(path):
    imgpath = {'image_file':open(path, 'rb')}
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  
    payload = {'api_key': 'jm499WpdnMzlXeUeKRBuQuAUryJvyBxN',  
               'api_secret':'EuKoxYYPgXBIiSMGrjhQsekKCmpuFT5O',  
               'return_landmark': 2,  
               'return_attributes':'headpose,eyestatus,mouthstatus'} 
    r = requests.post(url,files=imgpath,data=payload)  
    data=json.loads(r.text)
    return(data)

def drawlandmark(imgrgb,landmarks):
    for i in landmarks:
        cor=landmarks[i]
        x=cor["x"]
        y=cor["y"]
        cv2.circle(imgrgb,(x,y),2,(0,0,255),-1)
    #cv2.imwrite(savepath+objFilePath.split('/')[-1][0:-3]+'jpg',imgrgb)
    #for d in range(0,len(landmark)):
        #cv2.circle(imgrgb,(landmark[d,0],imgrgb.shape[0]-landmark[d,1]),2,(0,0,255),-1)
    return(imgrgb)

def readobjnormal(objFilePath):
    with open(objFilePath) as file:
        points = []
        faceraw = []
        while 1:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "v":
                points.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "f":
                faceraw.append((strs[1],strs[2],strs[3].split("\n")[0]))
    points = np.array(points)
    faceraw=np.array(faceraw,dtype=int)-1
    return points,faceraw
    

model=np.array([[-51,30,-42],[-18,31,-32],[18,31,-32],
[51,30,-42],[0,32,-20],[0,0,0],[-23,-34,-25],[23,-34,-25]])
##exr,enr,enl,exl,n,prn,chr,chl

modelb=np.array([[-51,30,-42],[-18,31,-32],[18,31,-32],
[51,30,-42],[0,0,0],[-23,-34,-25],[23,-34,-25]])