import cv2, os
SCALAR_RED = (0.0, 0.0, 255.0)
inputFolder = r'C:\Users\Hi\Documents\drive\darknet\img'
# outputFolder = r''
for fileName in os.listdir(inputFolder):
    if 'jpg' in fileName:
        if not fileName.startswith('0'):
            imgPath = os.path.join(inputFolder, fileName)
            imgOriginalScene = cv2.imread(imgPath)
            txtFile = fileName.replace('jpg', 'txt')
            txtPath = os.path.join(inputFolder, txtFile)
            h, w, _ = imgOriginalScene.shape
            with open(txtPath) as f:
                line= f.readline()
                l = line.split(' ')
                centerX = float(l[1]) * w
                centerY = float(l[2]) * h
                width = float(l[3]) * w
                height = float(l[4]) * h
                config = (tuple((centerX, centerY)), tuple((width, height)), 0)
                p2fRectPoints = cv2.boxPoints(config)
                cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
                cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
                cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
                cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
                cv2.imshow("imgOriginalScene", imgOriginalScene)
                cv2.waitKey(-1)
                cv2.destroyAllWindows()
            f.close()

