import cv2, os
SCALAR_RED = (0.0, 0.0, 255.0)
# imgPath = r'C:\Users\Hi\Documents\drive\darknet\img\6742743_LpnImg_220190802120415.jpg'
inputFolder = r'C:\Users\Hi\Documents\drive\darknet\img'
# outputFolder = r''
for fileName in os.listdir(inputFolder):
    if 'jpg' in fileName:
        if not fileName.startswith('0'):
            imgPath = os.path.join(inputFolder, fileName)
            imgOriginalScene = cv2.imread(imgPath)
            txtFile = fileName.replace('jpg', 'txt')
            txtPath = os.path.join(inputFolder, txtFile)

            # imgPath = r'C:\Users\Hi\Desktop\cbimage.jpg'
            # imgOriginalScene = cv2.imread(imgPath)
            # txtPath = r'C:\Users\Hi\Documents\drive\darknet\img\6742743_LpnImg_220190802120415.txt'
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
# l = [210.1811981201, 268.5507774353, 290.9268951416, 347.3855495453]
# centerX = float( (l[0] + l[2])/2 )
# centerY = float(( l[1] + l[3] )/2 )
# width = l[2] - l[0]
# height = l[3] - l[1]
# config = (tuple((centerX, centerY)), tuple((width, height)), 0)
# p2fRectPoints = cv2.boxPoints(config)
# cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
# cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
# cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
# cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# cv2.imshow("imgOriginalScene", imgOriginalScene)
# cv2.waitKey(-1)
# cv2.destroyAllWindows()
#
# print(ord(''))
# print(chr(27))

