import os, sys
import cv2
import time
import numpy as np
import pytesseract
from PIL import Image
import cv2
import argparse
import numpy as np
from Preprocess import *

# inputFolder = r"C:\Users\Hi\Documents\drive\labelImg-master\downloads\bien so xe o to"
inputFolder = r'C:\Users\Hi\Desktop\Lpn\20190723'
# outputFolder = r"F:\LpAfterDetection"
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hi\Documents\drive\tesseract\build\bin\Debug\tesseract.exe'
# setting_confidence = 1

#################################################################################
#params
configPath= r'yolo_obj.cfg'
weightsPath = r'C:\Users\Hi\Desktop\weights from YOLO\yolo_obj_2000.weights'
classesPath = r'yolov3.txt'

scale = 0.00392
classes = None
f = open(classesPath, 'r')
classes = [line.strip() for line in f.readlines()]
f.close()
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNet(weightsPath, configPath)
####Read Video
videoPath = r'C:\Users\Hi\Desktop\Lpn\20190723\outpy.avi'
cap = cv2.VideoCapture(videoPath)
#######Read Image
# imgPath = r'C:\Users\Hi\Documents\drive\darknet\img\6612199_LpnImg_220190717000455.jpg'
# image = cv2.imread(imgPath)

###################################################################################
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label+':', (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(img, str(int(confidence * 100)) + '%',(x +100, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return

# while(cap.isOpened()):
#     ret, image = cap.read()
for fileName in os.listdir(inputFolder):
    if ('jpg' in fileName) or ('png' in fileName):
        imgPath = os.path.join(inputFolder, fileName)
    else:
        continue
    image = cv2.imread(imgPath)

   #Xam hoa anh va tao anh xam 3 chanels
    image, imgThresh = preprocess(image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.stack((image,)*3, axis=-1)

    Width = image.shape[1]
    Height = image.shape[0]
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold, top_k=1)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

    cv2.imshow("object detection", image)
    # time.sleep(2)
    cv2.waitKey()

    # cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()


