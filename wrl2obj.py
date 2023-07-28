
import pymeshlab
import os
import sys
import glob
objFilePath=sys.argv[1]
ms.load_new_mesh(objFilePath)
ms.convex_hull()
ms.save_current_mesh(objFilePath[0:-3]+'obj')