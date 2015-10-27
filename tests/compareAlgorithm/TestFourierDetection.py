import unittest
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox
from src.service.CrosswalkLoader import CrosswalkLoader
from src.service.AlgorithmComparer import AlgorithmComparer
from src.detection.fourier.BoxWalker import BoxWalker
from src.base.Constants import Constants
from src.service.TilesLoader.TileProxy import TileProxy


class TestFourierDetection(unittest.TestCase):

    def test_fourierdetection(self):
        proxy = self.getRappiProxy()
        bbox = proxy.bbox

        crosswalLoader = CrosswalkLoader()


        walker = BoxWalker(bbox)
        walker.loadStreets()
        walker.proxy = proxy

        crosswalks = crosswalLoader.getCrosswalkNodes(bbox)
        detectedNodes = walker.walk()

        algorithmComparer = AlgorithmComparer(detectedNodes,crosswalks)

        bigTile = proxy.getBigTile2()

        blue = (255,0,0)
        green = (0,255,0)
        algorithmComparer.drawNodes(bigTile, detectedNodes, blue)
        algorithmComparer.drawNodes(bigTile, crosswalks, green)

        bigTile.plot()
        self.assertTrue(algorithmComparer.getHits() > 0)

    def test_fourierdelstection2(self):
        crosswalLoader = CrosswalkLoader()

        bbox = self.Glarus()
        walker = BoxWalker(bbox)
        walker.loadTiles()
        walker.loadStreets()

        crosswalks = crosswalLoader.getCrosswalkNodes(bbox)
        detectedNodes = walker.walk()

        algorithmComparer = AlgorithmComparer(detectedNodes,crosswalks)

        bigTile = walker.proxy.getBigTile2()

        blue = (255,0,0)
        green = (0,255,0)
        algorithmComparer.drawNodes(bigTile, detectedNodes, blue)
        algorithmComparer.drawNodes(bigTile, crosswalks, green)

        bigTile.plot()
        self.assertTrue(algorithmComparer.getHits() > 0)

    def getRappiProxy(self):
        path = Constants.SerializationFolder + "rapperswil.serialize"
        return TileProxy.fromFile(path)

    def Aarrau(self):
        return Bbox(8.043251, 47.389006, 8.049301, 47.392061)

    def Biel(self):
        return Bbox(7.240067, 47.132898, 7.245366, 47.136229)

    def Lyss(self):
        return Bbox(7.304337, 47.072818, 7.308200, 47.075229)

    def RappiConfuctionMatrix(self):
        return Bbox(8.814650, 47.222553, 8.825035, 47.228935)

    def StGallen(self):
        return Bbox(9.380092, 47.423250, 9.382681, 47.425163)

    def Glarus(self):
        return Bbox(9.065367, 47.039350, 9.069577, 47.043968)

    def Kloten(self):
        return Bbox(8.542078, 47.418137, 8.553164, 47.423409)