from src.base.Tile import Tile, Bbox
from src.data.TileLoader import TileLoader
import unittest



class NodeTest(unittest.TestCase):
    def test_save50images(self):
        loader = TileLoader(self.lausanne2())
        tile = loader.get_big_tile()
        tile.save50Images("/home/osboxes/Documents/squaredImages/generatedNo/lausanne2/" ,"lausanne2")


    def Luzern(self):
        return Bbox(8.301307, 47.046349, 8.305528, 47.051053)

    def ChurBhfAltstadt(self):
        #TrainSet
        return Bbox(9.528281, 46.850342, 9.532599, 46.853980)
    def Zurich2(self):
        #Trainset
        return Bbox(8.530470, 47.366188, 8.537807, 47.372053)

    def HinwilQuartier(self):
        return Bbox(8.840301, 47.297006, 8.851266, 47.300455)

    def NiederurnenQuartier(self):
        return Bbox(9.050981, 47.122531, 9.055832, 47.125728)

    def BernAltstadt(self):
        return Bbox(7.441249, 46.948004, 7.444076, 46.950337)

    def RappiAltstadt(self):
        return Bbox(8.816654, 47.226393, 8.818284, 47.227991)

    def zh3(self):
        return Bbox(8.547723, 47.370117, 8.550090, 47.371060)


    def zhx(self):
        return Bbox(8.484491, 47.394720, 8.489919, 47.396429)

    def Lyss(self):
        #Trainset
        return Bbox(7.304337, 47.072818, 7.308200, 47.075229)

    def zh4(self):
        return Bbox(8.536479, 47.375204, 8.540248, 47.376933)

    def zh6(self):
        return Bbox(8.533828, 47.386608, 8.535850, 47.387211)

    def zh_quartier1(self):
        return Bbox(8.528067, 47.393102, 8.532648, 47.394939)

    def lugano_innenstadt(self):
        return Bbox(8.950611, 46.004539, 8.956414, 46.006190)
    def zh_quartier1(self):
        return Bbox(8.528067, 47.393102, 8.532648, 47.394939)

    def lausanne2(self):
        return Bbox(6.653206, 46.520170, 6.659357, 46.523023)