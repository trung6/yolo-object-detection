#USAGE:
#You need to modify 4 following directories to be suitable for your case, include: trainTxtPath, testTxtPath, inputFolder, outputFolder
#when an image appears,
#mouse-click in bottom-left point of license and move to top-right point of license
#I will show what you've just cropped
# if you cropped wrongly, plese press "r" to close the img with bounding box and crop again
# when you crop right, close the img with bounding box, then press "c" for next picture or exit when there is no picture else.

import argparse
import cv2
import shutil, sys
import os
import matplotlib.pyplot as plt

debugCheck = True
count = 0
#modify 4 following directories to be suitable for your case
trainTxtPath = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\train.txt")#txt file contains paths link to training data
testTxtPath = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\test.txt")#txt file contains paths link to testing data or validating data.

inputFolder = os.path.abspath(r"images")#directory contains raw images(data).

#if genTrain == True, we are generating Training Dataset.
#if genTrain == False, we are generating Testing Dataset.
genTrain = False

#directory contains images(data) which were handled manually.'
if genTrain == True:
    outputFolder = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\img")
else:
    outputFolder = os.path.abspath(r"C:\Users\Hi\Documents\drive\darknet\imgTest")

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
countNegative = 0
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, count
    img = cv2.imread(imgPath)

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [[x, y]]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
    
    # record the ending (x, y) coordinates and indicate that
    # the cropping operation is finished
        count+=1
        refPt.append([x, y])
        cropping = False
        width = (float(refPt[-1][0] - refPt[-2][0]))
        height = (float(refPt[-1][1] - refPt[-2][1]))
        centerX = abs(float((refPt[-1][0] + refPt[-2][0])/2))
        centerY = abs(float((refPt[-1][1] + refPt[-2][1])/2))
        h, w, _ = img.shape
    
    #show what you've just cropped
    #integer argument for 4 below parameters
        bounding_x1 = int(refPt[-2][0])
        bounding_y1 = int(refPt[-2][1])
        bounding_w = int(width)
        bounding_h = int(height)
        bounding_x2 = bounding_x1 + bounding_w
        bounding_y2 = bounding_y1 + bounding_h
        cv2.rectangle(img, (bounding_x1, bounding_y1), (bounding_x2, bounding_y2), (0, 0xFF, 0), 2)
        if(count % 1000 == 0):
            warning = "image + {0}".format(count)
            cv2.putText(img, warning, (bounding_x1 - 10, bounding_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0xFF, 0), 2 )
        cv2.imshow("img",img)
    #press "r" to close this window.
        key = cv2.waitKey(1) & 0xFF
        if key== ord("r"):
            cv2.destroyWindow("img")
    
    #if you cropped wrongly, plese close the img with bounding box and crop again
    #when you crop right, close the img with bounding box, then press "c"
        normalizedHeight = abs(float(height/h))
        normalizedWidth = abs(float(width/w))
        normalizedCenterX = float(centerX / w)
        normalizedCenterY = float(centerY/ h)
        line = "0 {0} {1} {2} {3}".format(normalizedCenterX, normalizedCenterY, normalizedWidth, normalizedHeight)

        if debugCheck == True:
           print(line)

    # path to txt file that contains label for image detector
    # labels for Yolo detector will be saved in txt files.
    # in each such file, there is a line in format: "class ID (int), normalizedCenterX, normalizedCenterY, normalizedWidth, normalizedHeight"
        file = open(outputPath, 'w')
        file.writelines(line)
        file.close()
    return
##############################################################################################################

for fileName in os.listdir(inputFolder):

    outFileName = fileName.replace('jpg', 'txt')
    imgPath = os.path.join(inputFolder, fileName)
    imgPathOut = os.path.join(outputFolder, fileName)
    outputPath = os.path.join(outputFolder, outFileName)# path to txt file that contains label for image detector

# construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--imagePath", required=False, default=imgPath, help="Path to the image")
    ap.add_argument("-o", "--outputPath", required=False, default=outputPath, help="Path to the txt file")
    ap.add_argument("-fn", "--fileName", required= False, default= fileName, help = "Name of image")
    ap.add_argument("-ipo", "--imgPathOut", required=False, default=imgPathOut, help = "Save image to new place")
    args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
    image = cv2.imread(args["imagePath"])
    #clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'o' key is pressed, omit this image because there is no license plate in it.
        if key == ord("o"):
            break

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            # path in train.txt/test.txt
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
            break

        # if the "b" is pressed, blank txt file will be created in outputFolder
        elif key == ord("b"):

            # empty .txt file
            line = ""
            file = open(outputPath, 'w')
            file.writelines(line)
            file.close()

            # path in train.txt/test.txt
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
            break

    # close all open windows
    cv2.destroyAllWindows()
