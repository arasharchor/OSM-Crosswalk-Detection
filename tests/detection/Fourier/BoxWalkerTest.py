from src.detection.fourier.BoxWalker import BoxWalker
import unittest
from src.base.Bbox import Bbox
from src.base.Constants import Constants
from src.base.Tile import Tile
from src.service.TilesLoader.TileProxy import TileProxy




class TestImageLoader(unittest.TestCase):

    def testBoxWalkerLuzern(self):
        walker = BoxWalker(self.Lyss())
        walker.loadTiles()
        walker.loadStreets()

        crosswalkNodes = walker.walk()

        self.printResults(walker.tile, crosswalkNodes)

    def test_Boxwalker(self):
        proxy = self.getRappiProxy()
        bbox = proxy.bbox
        walker = BoxWalker(bbox)
        walker.proxy = proxy
        walker.loadStreets()

        crosswalkNodes = walker.walk()

        proxy = walker.proxy
        tile = proxy.getBigTile(bbox.getDownLeftPoint(),bbox.getUpRightPoint())
        tile.startDrawing()
        for node in crosswalkNodes:
            point = node.toPoint()
            tile.drawPoint(point)

        tile.stopDrawing()
        tile.plot()
        tile.image.save("boxwalkertest.png")

        print str(len(crosswalkNodes)) + " crosswalks found!"

    def printResults(self, tile, crosswalkNodes):
        tile.startDrawing()
        for node in crosswalkNodes:
            point = node.toPoint()
            tile.drawPoint(point)

        tile.stopDrawing()
        tile.plot()

    def test_Saveimages(self):
        bbox = self.Lyss()
        walker = BoxWalker(bbox)
        walker.loadTiles()
        walker.loadStreets()

        walker.saveImages()

    def getRappiProxy(self):
        #Trainset
        path = Constants.SerializationFolder +  "rapperswil.serialize"# "zurichBellvue.serialize"
        return TileProxy.fromFile(path)

    def ZurichBellvue(self):
        #Trainset
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Rappi(self):

        return Bbox(8.814650, 47.222553, 8.825035, 47.228935)

    def Luzern(self):
        return Bbox(8.301307, 47.046349, 8.305528, 47.051053)

    def BernAltStadt(self):
        #TrainSet
        return Bbox(7.444389, 46.947913, 7.448316, 46.949693)

    def ChurBhfAltstadt(self):
        #TrainSet
        return Bbox(9.528281, 46.850342, 9.532599, 46.853980)

    def Zurich2(self):
        #Trainset
        return Bbox(8.530470, 47.366188, 8.537807, 47.372053)

    def BernKoeniz(self):
        return Bbox(7.406960, 46.920077, 7.415008, 46.924285)

    def Lausanne(self):
        return Bbox(6.555186, 46.508591, 6.563499, 46.516437)

    def Lyss(self):
        #Trainset
        return Bbox(7.304337, 47.072818, 7.308200, 47.075229)

    def zh1(self):
        return Bbox(8.522537, 47.375915, 8.526331, 47.376639)

    def zh_schlieren_test(self):
        return Bbox(8.441207, 47.394649, 8.449643, 47.399710)

    def zh_hardbrucke_test(self):
        return Bbox(8.517822, 47.386440, 8.520540, 47.388008)

    def zh_hardbrucke_test2(self):
        return Bbox(8.521436, 47.390424, 8.524241, 47.391289)

    def zh_quartier1(self):
        return Bbox(8.528067, 47.393102, 8.532648, 47.394939)

    def zh_europabrucke(self):
        return Bbox(8.492554, 47.391842, 8.503230, 47.394553)

    def winti1(self):
        return Bbox(8.716155, 47.511909, 8.721038, 47.515722)

    def winti_innenstadt(self):
        return Bbox(8.723835, 47.497560, 8.733661, 47.501156)

    def thun_innenstadt(self):
        return Bbox(7.624835, 46.758937, 7.630741, 46.762592)

    def heiligkreuz(self):
        return Bbox(9.408957, 47.055055, 9.418505, 47.060288)

    def staefa(self):
        return Bbox(8.729157, 47.233379, 8.741170, 47.238049)

    def zh_buchs(self):
        return  Bbox(8.432206, 47.456906, 8.441375, 47.461262)

    def ag_baden(self):
        return Bbox(8.308925, 47.464633, 8.317642, 47.467798)

    def ag_baden2(self):
        return Bbox( 8.314834, 47.462698, 8.324612, 47.468880)

    def zh_frauental_quartier(self):
        return Bbox(8.507748, 47.355263, 8.510934, 47.358226)

    def zh_quartier2(self):
        return Bbox(8.520495, 47.369944, 8.523971, 47.372846)