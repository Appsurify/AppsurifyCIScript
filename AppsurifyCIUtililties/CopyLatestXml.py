#!/usr/bin/env python3
#requires python>3.6

import os
import sys
import shutil


inputFolder=""
outputFolder=""
fileName=""
copyName=""

c=0

if len(sys.argv) > 1 :
    c=len(sys.argv)
    for k in range(1,c):
        if sys.argv[k] == "--inputFolder":
            inputFolder = sys.argv[k+1]
        if sys.argv[k] == "--outputFolder":
            outputFolder = sys.argv[k+1]
        if sys.argv[k] == "--fileName":
            fileName = sys.argv[k+1]
        if sys.argv[k] == "--copyName":
            copyName = sys.argv[k+1]

if inputFolder == "":
    print("no inputFolder specified")
    exit(1)
if outputFolder == "":
    print("no outputFolder specified")
    exit(1)
if fileName == "":
    print("no fileName specified")
    exit(1)
if copyName == "":
    print("no copyName specified")
    exit(1)

if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

files = os.listdir(inputFolder)
paths = [os.path.join(inputFolder, basename) for basename in files]

latestFolder = (max(paths, key=os.path.getctime))
fileToCopy = os.path.join(latestFolder, fileName)
copiedFileLocation = os.path.join(outputFolder, copyName)
shutil.copy2(fileToCopy, copiedFileLocation)