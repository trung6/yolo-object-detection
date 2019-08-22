import cv2, os
from PIL import Image
import random

inputFolder = r'C:\Users\Hi\Documents\drive\darknet\imgTest'
outputFolder = r'F:\LpCrop'
count = 0
listFile = os.listdir(inputFolder)
for fileName1 in os.listdir(inputFolder):
    fileName = random.choice(listFile)
    if (('jpg' in fileName) and ('Lpn' in fileName)):
        count+=1
        imgPath = os.path.join(inputFolder, fileName)
        fileTxt = fileName.replace('jpg', 'txt')
        txtPath = os.path.join(inputFolder, fileTxt)
        img = Image.open(imgPath)
        w, h = img.size
        f = open(txtPath, 'r')
        line = f.readline()
        l = line.split(' ')
        try:
            centerX = float(l[1]) * w
            centerY = float(l[2]) * h
            width = float(l[3]) * w
            height = float(l[4]) * h
        except:
            centerX = 0
            centerY = 0
            width = 0
            height = 0
        left = centerX - width/2
        top = centerY -  height/2
        right = left + width
        bottom = top + height
        # config = (tuple((centerX, centerY)), tuple((width, height)), 0)
        # p2fRectPoints = cv2.boxPoints(config)
        f.close()
        imgPathOut = os.path.join(outputFolder, fileName)
        lpImg = img.crop((left, top, right, bottom))
        try:
            lpImg.save(imgPathOut)
        except:
            continue
    # if count == 500:
    #     break


