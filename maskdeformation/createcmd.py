from matplotlib.path import Path
import pandas as pd
import numpy as np
import glob
import os
from math import *
import sys

files=glob.glob(os.path.join("/data/dusiyuan/CASdata/tz/",'*.csv'))
f=open("/data/dusiyuan/3Dface/maskdeformation/cmd",'w')
for file in files:
    f.write("python 2.maskdeformation_onefile.py "+file+"\n")

f.close()