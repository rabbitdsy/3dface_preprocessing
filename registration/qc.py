#manual selection

from tkinter import *
import tkinter as tk
import glob
import os
from PIL import Image, ImageTk
import numpy as np
import pandas as pd


def tag_complete():
    global tag
    tag=1
    myWindow.destroy()
    
def tag_part():
    global tag
    tag=0.5
    myWindow.destroy()

def tag_cover():
    global tag
    tag=0
    myWindow.destroy()
    
def tag_exit():
    global tag
    tag=-9
    myWindow.destroy()
    
    

files=pd.read_table("D:\\3Dface\\qingdao2\\files\\dup.txt",  encoding="gbk")
tmp1=pd.DataFrame(files)
tmp2=pd.DataFrame(files)
temp=pd.concat([tmp1,tmp2],axis=1)
tag=0

for i in range(0,10):
    print(i)
    myWindow = tk.Tk()
    #myWindow = tk.Toplevel()
    myWindow.title('Python GUI Learning')
    b1=Button(myWindow, text='通过', bg="green", width=10, height=5,command=tag_complete)
    b1.grid(row=1, column=1, sticky=W, padx=5,pady=5)
    b2=Button(myWindow, text='面中ok',bg="grey", width=10, height=5,command=tag_part)
    b2.grid(row=2, column=1, sticky=W, padx=5, pady=5)
    b3=Button(myWindow, text='不过关',bg="red", width=10, height=5,command=tag_cover)
    b3.grid(row=3, column=1, sticky=W, padx=5, pady=5)
    b4=Button(myWindow, text='退出',bg="red", width=10, height=5,command=tag_exit)
    b4.grid(row=4, column=1, sticky=W, padx=5, pady=5)

    img_open = Image.open(files.iloc[i,0])
    #img_resize=img_open.resize((500,500))
    #img_png = ImageTk.PhotoImage(img_resize)
    img_png = ImageTk.PhotoImage(img_open)
    label_img = tk.Label(myWindow, image = img_png,bg = 'white',bd =20,height=350,width=400)
    label_img.grid(row=0, column=0, sticky=W, padx=5,pady=5)
    if tag==-9:
        myWindow.mainloop()
        break
    temp.iloc[i,1]=tag
    myWindow.mainloop()
    
temp.to_csv("D:\\3Dface\\qingdao2\\files\\dup2.txt",sep=",",encoding=("gbk"))


#%%
#files=glob.glob(os.path.join("D:\\3Dface\\qingdao2\\step4d\\image\\",'*.png'))
#files.sort()
#f=open("D:\\3Dface\\qingdao2\\files\\dup.txt",'w')
#for file in files:
#    f.write(file+'\n')
#f.close()