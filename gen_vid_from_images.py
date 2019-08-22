import cv2
import os, sys
import time
import matplotlib.pyplot as plt
inputFolder = r'C:\Users\Hi\Desktop\Lpn\20190723'
outPath = os.path.join(inputFolder,'outpy1.avi')
w = 1280
h = 960
out = cv2.VideoWriter(outPath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (w, h))
for fileName in os.listdir(inputFolder):
    imgPath = os.path.join(inputFolder, fileName)
    for i in range(100):
        img = cv2.imread(imgPath)
        out.write(img)

out.release()
cv2.destroyAllWindows()
