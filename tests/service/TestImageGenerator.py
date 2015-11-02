import unittest
import os.path

from src.service.ImageGenerator import ImageGenerator
from src.service.StreetImageGenerator import StreetImageGenerator
from src.base.Bbox import Bbox


class TestImageGenerator(unittest.TestCase):

    def testZebraBasel(self):
        #path = "/home/murthy/Projects/SA/images/positive/basel_small/"
        #path = "/home/murthy/Projects/SA/images/positive/zuerich_small/"
        path = "/home/osboxes/Documents/squaredImages/generated/"

        #bbox = Bbox('7.559269', '47.551828', '7.612397', '47.571766') #basel, Frauenfeld, Soloturn
        bbox = Bbox(7.121068, 46.787844, 7.177903, 46.820269)
    #bbox = Bbox('6.128354', '46.187747', '6.157744', '46.203332')
        #bbox = Bbox(8.570083, 47.387947, 8.637695, 47.426400) #Duebendorf
        #bbox = Bbox(6.114341, 46.176792, 6.159574, 46.204077) #Genf
        #bbox = Bbox(8.481206, 47.376824, 8.525474, 47.395859) #ZH1
        #bbox = Bbox(8.474892, 47.361230, 8.566503, 47.383488) #ZH2

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])

    def testStreetGenerator(self):
        path = "/home/osboxes/Documents/squaredImages/generatedNo/"

        #bbox = Bbox('7.559269', '47.551828', '7.612397', '47.571766') #basel
        #bbox = Bbox('7.559269', '47.561828', '7.562397', '47.571766') #kliBasel
        #bbox = Bbox('8.516459', '47.366062', '8.546671', '47.386928')
        #bbox = Bbox('6.128354', '46.187747', '6.157744', '46.203332')
        #bbox = Bbox(8.570083, 47.387947, 8.637695, 47.426400) #Duebendorf
        bbox = Bbox(6.114341, 46.176792, 6.159574, 46.204077) #Genf
        #bbox = Bbox(8.481206, 47.376824, 8.525474, 47.395859) #ZH1
        #bbox = Bbox(8.474892, 47.361230, 8.566503, 47.383488) #ZH2

        imageGenerator = StreetImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])
