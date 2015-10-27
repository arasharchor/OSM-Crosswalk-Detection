import cv2
from PIL import Image
import numpy as np
from src.base.Bbox import Bbox
from matplotlib import pyplot as plt
from src.base.Node import Node
from geopy import Point
from src.base.Constants import Constants
import pickle

class Tile:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox
        self.isDrawing = False

    def startDrawing(self):
        self.drawImage = Tile.getCv2Image(self.image)
        self.isDrawing = True

    def stopDrawing(self):
        self.image = self.__getPilImage(self.drawImage)
        self.isDrawing = False

    def drawLine(self, point1, point2):
        if(not self.isDrawing): raise Exception("Enter startDrawing first")
        p1 = self.getPixel(point1)
        p2 = self.getPixel(point2)

        cv2.line(self.drawImage,p1,p2,(255,0,0),5)

    def drawPoint(self, point):
        if(not self.isDrawing): raise Exception("Enter startDrawing first")

        p1 = self.getPixel(point)
        cv2.circle(self.drawImage,p1,10,(0,255,0), -1)

    def drawColorPoint(self, point, color):
        if(not self.isDrawing): raise Exception("Enter startDrawing first")

        p1 = self.getPixel(point)
        cv2.circle(self.drawImage,p1,10,color, -1)


    def getPixel(self, point):
        imagewidth = float(self.bbox.right) - float(self.bbox.left)
        imageheight = float(self.bbox.top) - float(self.bbox.bottom)

        x = point.longitude - float(self.bbox.left)
        y = point.latitude - float(self.bbox.bottom)

        pixelX =  int(self.image.size[0] * (x/imagewidth))
        pixelY = self.image.size[1] - int(self.image.size[1] * (y/imageheight))
        return (pixelX, pixelY)

    def getNode(self, pixel):
        x = pixel[0]
        y = pixel[1]
        xCount = self.image.size[0]
        yCount = self.image.size[1]
        yPart = (yCount - y) / float(yCount)
        xPart = x / float(xCount)

        latDiff = float(self.bbox.top) - float(self.bbox.bottom)
        lonDiff = float(self.bbox.right) - float(self.bbox.left)

        lat = float(self.bbox.bottom) + latDiff*yPart
        lon = float(self.bbox.left) + lonDiff*xPart

        return Node.create(Point(lat, lon))

    def getCentreNode(self):
        diffLat = self.bbox.getUpRightPoint().latitude - self.bbox.getDownLeftPoint().latitude
        diffLon = self.bbox.getUpRightPoint().longitude - self.bbox.getDownLeftPoint().longitude
        middle = Point(self.bbox.getDownLeftPoint().latitude + diffLat/2, self.bbox.getDownLeftPoint().longitude + diffLon/2)
        return Node.create(middle)


    @staticmethod
    def getCv2Image(pilimg):
       return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


    def __getPilImage(self, cv2img):
        cv2_im = cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB)

        return Image.fromarray(cv2_im)

    def getSquaredImages(self, node1, node2):
        PIXELCOUNT = Constants.squaredImage_PixelPerSide / 3
        METER_PER_PIXEL = Constants.METER_PER_PIXEL
        stepDistance = PIXELCOUNT * METER_PER_PIXEL

        node1 = self.__ajustNodeToBoarder(node1)
        node2 = self.__ajustNodeToBoarder(node2)

        assert self.bbox.inBbox(node1.toPoint())
        assert self.bbox.inBbox(node2.toPoint())

        distanceBetweenNodes = node1.getDistanceInMeter(node2)

        squaresTiles = []
        for i in range(0, int(distanceBetweenNodes/stepDistance) + 1):
            currentDistance = stepDistance * i

            currentNode = node1.stepTo(node2, currentDistance)
            currentNode = self.__ajustNodeToBoarder(currentNode)

            assert self.bbox.inBbox(currentNode.toPoint())

            tile = self.__getSquaredImage(currentNode.toPoint())
            squaresTiles.append(tile)


        return squaresTiles

    def __ajustNodeToBoarder(self, node):
        xCount = self.image.size[0]
        yCount = self.image.size[1]
        pixel = self.getPixel(node.toPoint())
        resultPixel = [pixel[0], pixel[1]]

        borderPixel = Constants.squaredImage_PixelPerSide
        if(pixel[0] < borderPixel): resultPixel[0] = borderPixel
        if(pixel[1] < borderPixel): resultPixel[1] = borderPixel
        if(yCount - pixel[1] < borderPixel):
            resultPixel[1] = yCount - borderPixel
        if(xCount - pixel[0] < borderPixel):
            resultPixel[0] = xCount - borderPixel

        newnode = self.getNode(resultPixel)


        return newnode


    def getSquaredImage(self, centrePoint, PIXEL_PER_SIDE):
        #PIXEL_PER_SIDE = Constants.squaredImage_PixelPerSide
        METER_PER_PIXEL = Constants.METER_PER_PIXEL
        DISTANCE = PIXEL_PER_SIDE * METER_PER_PIXEL

        centreNode = Node.create(centrePoint)
        leftDown = centreNode.addMeter(-DISTANCE/2,-DISTANCE/2)
        rightTop = centreNode.addMeter(DISTANCE/2,DISTANCE/2)


        leftDown = self.__ajustNodeToBoarder(leftDown)
        rightTop = self.__ajustNodeToBoarder(rightTop)

        assert self.bbox.inBbox(leftDown.toPoint())
        assert self.bbox.inBbox(rightTop.toPoint())


        box = Bbox()
        box.set(leftDown.toPoint(), rightTop.toPoint())
        return self.getSubTile(box)

    def getSubTile(self, bbox):
        if(not(self.bbox.inBbox(bbox.getDownLeftPoint()) and self.bbox.inBbox(bbox.getUpRightPoint()))):
            raise Exception("given bbox is out of bbox of this tile")

        cv2Image = Tile.getCv2Image(self.image)

        p1 = self.getPixel(bbox.getDownLeftPoint())
        p2 = self.getPixel(bbox.getUpRightPoint())

        cropped = cv2Image[p2[1]:p1[1], p1[0]:p2[0]]

        assert cropped.size > 0


        cropped = self.__getPilImage(cropped)

        return Tile(cropped,bbox)

    def getExtendedSubTile(self, bbox):
        pld = bbox.getDownLeftPoint()
        pru = bbox.getUpRightPoint()
        pixelLeftDown = self.getPixel(pld)
        pixelRightUp = self.getPixel(pru)

        correction = Constants.squaredImage_PixelPerSide*1

        x1 = pixelLeftDown[0] - correction
        y1 = pixelLeftDown[1] + correction
        if(x1 < 0): x1 = 0
        if(y1 > self.image.size[1]): y1 = self.image.size[1] -1

        pixelLeftDown = (x1, y1)

        x2 = pixelRightUp[0] + correction
        y2 = pixelRightUp[1] - correction

        if(x2 > self.image.size[0]): x2 = self.image.size[0] -1
        if(y2 < 0): y2 = 0
        pixelRightUp = (x2, y2)


        p1 = self.getNode(pixelLeftDown).toPoint()
        p2 = self.getNode(pixelRightUp).toPoint()
        bbox = Bbox()
        bbox.set(p1, p2)
        return self.getSubTile(bbox)


    def save50Images(self, dir_path, prefix):
        (width, height) = self.image.size

        for x in range(width/50 -1):
            for y in range(height/50 -1):
                x1 = 50*x
                y1 = 50*y
                x2 = x1 + 50
                y2 = y1 + 50
                img = self.image.crop((x1, y1, x2, y2))
                img.save(dir_path + prefix + "img" + str(x) + ","+ str(y) + ".png")

    def plot(self):
        plt.imshow(self.image)
        plt.show()
