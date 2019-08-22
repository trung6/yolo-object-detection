# USAGE:
# You need to modify 4 following directories to be suitable for your case, include: trainTxtPath, testTxtPath, inputFolder, outputFolder
# when an image appears,
# mouse-click in bottom-left point of license and move to top-right point of license
# I will show what you've just cropped
# if you cropped wrongly, plese press "r" to close the img with bounding box and crop again
# when you crop right, close the img with bounding box, then press "c" for next picture or exit when there is no picture else.

import argparse
import cv2
import shutil, sys
import os
import matplotlib.pyplot as plt

debugCheck = True

# modify 4 following directories to be suitable for your case
trainTxtPath = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\train.txt")  # txt file contains paths link to training data
testTxtPath = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\test.txt")  # txt file contains paths link to testing data or validating data.
inputFolder = os.path.abspath(r"F:\val2017")  # directory contains raw images(data).

# if genTrain == True, we are generating Training Dataset.
# if genTrain == False, we are generating Testing Dataset.
genTrain = False
if genTrain == False:
    outputFolder = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\imgTest")
else:
    outputFolder = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\img")

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
countNegative = 0
##############################################################################################################

for fileName in os.listdir(inputFolder):
    countNegative +=1

    outFileName = fileName.replace('jpg', 'txt')
    imgPath = os.path.join(inputFolder, fileName)
    imgPathOut = os.path.join(outputFolder, fileName)
    outputPath = os.path.join(outputFolder, outFileName)  # path to txt file that contains label for image detector

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--imagePath", required=False, default=imgPath, help="Path to the image")
    ap.add_argument("-o", "--outputPath", required=False, default=outputPath, help="Path to the txt file")
    ap.add_argument("-fn", "--fileName", required=False, default=fileName, help="Name of image")
    ap.add_argument("-ipo", "--imgPathOut", required=False, default=imgPathOut, help="Save image to new place")
    args = vars(ap.parse_args())
    #empty .txt file
    line = ""
    file = open(outputPath, 'w')
    file.writelines(line)
    file.close()
    #path in train.txt

    if genTrain == True:
        line2 = str("/content/img/") + fileName
        file2 = open(trainTxtPath, 'a')
    else:
        line2 = str("/content/imgTest/") + fileName
        file2 = open(testTxtPath, 'a')
    file2.write(line2)
    file2.write("\n")
    file2.close()

    # save image file to new location
    try:
        shutil.move(imgPath, imgPathOut)
    except OSError as e:
        print("OS error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(1)
    if countNegative >=900:
        break
print("Done")