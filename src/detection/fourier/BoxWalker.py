from src.detection.fourier.StreetWalker import StreetWalker
from src.data.TileLoader import TileLoader
from src.service.StreetLoader.StreetLoader import StreetLoader
import datetime
from src.detection.fourier.NodeMerger import NodeMerger
import src.detection.fourier.deep.Convnet


class BoxWalker:
    def __init__(self, bbox):
        self.bbox = bbox
        self.tile = None
        src.detection.fourier.deep.Convnet.initialize()

    def loadTiles(self):
        self.out("Loading images within bounding box")
        loader = TileLoader(self.bbox)
        self.tile = loader.get_big_tile()
        self.out("Images loaded")
    def loadStreets(self):
        self.out("Loading streets within bounding box")
        streetLoader = StreetLoader()
        self.streets = streetLoader.getStreets(self.bbox)
        self.out("Streets loaded")



    def walk(self):
        self.out("Start walking")
        streetsCount = len(self.streets)
        crosswalkNodes = []
        iCount = 0
        lastpercentage = 0
        for street in self.streets:
            iCount += 1
            streetwalker = StreetWalker(street, self.tile)
            streetResults =  streetwalker.walk()
            crosswalkNodes += streetResults
            percentage = (iCount / float(streetsCount)) *100
            if(lastpercentage + 1 < percentage):
                print  "walking: " + str(percentage) + "%"
                lastpercentage = percentage

        self.out("Finish walking")
        crosswalkNodes = self.mergeNodes(crosswalkNodes)
        return crosswalkNodes

    def mergeNodes(self, nodeList):
        merger = NodeMerger.fromNodeList(nodeList)
        return merger.reduce()

    def saveImages(self):
        tile = self.tile
        for street in self.streets:
            streetwalker = StreetWalker(street, tile)
            streetResults =  streetwalker.saveSquaredImages()

    def out(self,msg):
        print str(datetime.datetime.now()) + ": " + msg
