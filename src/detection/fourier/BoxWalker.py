from src.detection.fourier.StreetWalker import StreetWalker
from src.data.TileLoader import TileLoader
from src.service.StreetLoader.StreetLoader import StreetLoader
import datetime
from src.detection.fourier.NodeMerger import NodeMerger
import src.detection.fourier.deep.Convnet
import sys

class BoxWalker:
    def __init__(self, bbox):
        self.bbox = bbox
        self.tile = None
        self.start_time = None
        self.end_time = None
        self.start_time = datetime.datetime.now()
        src.detection.fourier.deep.Convnet.initialize()

    def loadTiles(self):
        self.out("Loading images within bounding box")
        loader = TileLoader(self.bbox)
        self.tile = loader.get_big_tile()
    def loadStreets(self):
        self.out("Loading streets within bounding box")
        streetLoader = StreetLoader()
        self.streets = streetLoader.getStreets(self.bbox)

    def walk(self):
        self.out("Start walking")
        print "   "
        streetsCount = len(self.streets)
        crosswalkNodes = []
        iCount = 0
        lastpercentage = 0
        nb_images = 0
        for street in self.streets:
            iCount += 1
            streetwalker = StreetWalker(street, self.tile)
            streetResults =  streetwalker.walk()
            nb_images += streetwalker.nb_images
            crosswalkNodes += streetResults
            percentage = (iCount / float(streetsCount)) *100
            if(lastpercentage + 1 < percentage):
                self.setConsoleState(percentage, len(crosswalkNodes))
                #print  "walking:", "{0:0.1f}".format(percentage), "%"
                lastpercentage = percentage

        self.out("Finish walking")
        crosswalkNodes = self.mergeNodes(crosswalkNodes)
        self.end_time = datetime.datetime.now()
        print "Time needed: " + str((self.end_time - self.start_time).seconds) + " seconds"
        print nb_images, "images predicted"
        return crosswalkNodes

    def setConsoleState(self, percentage, crosswalks_found):
        msg = "walking:" + "{0:0.1f}".format(percentage) + "% - " + str(crosswalks_found) + " crosswalks found"
        #sys.stdout.write("\r" + msg)
        #sys.stdout.flush()
        print msg

    def mergeNodes(self, nodeList):
        merger = NodeMerger.fromNodeList(nodeList)
        return merger.reduce()

    def saveImages(self):
        tile = self.tile
        for street in self.streets:
            streetwalker = StreetWalker(street, tile)
            streetResults = streetwalker.saveSquaredImages()

    def out(self,msg):
        print str(datetime.datetime.now()) + ": " + msg
