from geopy import Point
from src.base.Constants import Constants
from src.base.Node import Node

class Bbox:
    def __init__(self, left = 0, bottom = 0, right = 0, top = 0):
        self.bottom = str(bottom)
        self.left = str(left)
        self.top = str(top)
        self.right = str(right)
        self.__validation()

    def set(self, leftDownPoint, rightUpPoint):
        self.bottom = str(leftDownPoint.latitude)
        self.left = str(leftDownPoint.longitude)
        self.top = str(rightUpPoint.latitude)
        self.right = str(rightUpPoint.longitude)
        self.__validation()

    def __validation(self):
        if(float(self.bottom) > float(self.top)):
            temp = self.bottom
            self.bottom = self.top
            self.top = temp

        if(float(self.left) > float(self.right)):
            temp = self.left
            self.left = self.right
            self.right = temp


    def toString(self):
        return str(self.bottom) + "," + str(self.right) + "," + str(self.top)  + "," + str(self.left)

    def getMapquestFormat(self):
        return   str(self.left) + "," + str(self.bottom) + "," + str(self.right) + "," + str(self.top)

    def getMapquestFormat(self):
        return   str(self.left) + "," + str(self.bottom) + "," + str(self.right) + "," + str(self.top)

    def getBingFormat(self):
        return str(self.bottom) + "," + str(self.left) + "," + str(self.top) + "," + str(self.right)

    def printing(self):
        return "Bottom: " + str(self.bottom) + ", Right: " + str(self.right) + ", Top: " + str(self.top)  + ", Left: " + str(self.left)

    def getDownLeftPoint(self):
        return Point(self.bottom,self.left)

    def getUpRightPoint(self):
        return Point(self.top,self.right)

    def inBbox(self, point):
        lat = point.latitude
        lon = point.longitude

        inLat = lat >= float(self.bottom) and lat <= float(self.top)
        intLon = lon >= float(self.left) and lon <= float(self.right)

        return inLat and intLon

    def getCenterPoint(self):
        lon = float(self.left) + ((float(self.right) - float(self.left)) / 2)
        lat = float(self.bottom) + ((float(self.top) - float(self.bottom)) / 2)
        return Point(lat, lon)

    def getBboxExludeBorder(self, borderDistance):
        leftDownNode = Node.create(self.getDownLeftPoint())
        rightUpNode = Node.create(self.getUpRightPoint())

        newLeftDown = leftDownNode.addMeter(borderDistance, borderDistance)
        newRightUp = rightUpNode.addMeter(-borderDistance,-borderDistance)
        ret = Bbox()
        ret.set(newLeftDown.toPoint(),newRightUp.toPoint())
        return ret

