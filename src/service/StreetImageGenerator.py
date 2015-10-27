import os
from src.service.ImageLoader import ImageLoader
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.detection.fourier.CrosswalkDetector import CrosswalkDetector

class StreetImageGenerator:

    def __init__(self, destinationPath):
        self.destinationPath = destinationPath
        self.streetloader = StreetLoader()
        self.imageloader = ImageLoader()

    def generateCrosswalks(self, bbox):
        print "Downloading street informations"
        streets = self.streetloader.getStreets(bbox)

        print "Saving images"
        for street in streets:
            self.image_by_point(street.nodes[0].toPoint())
            self.image_by_point(street.nodes[1].toPoint())



    def image_by_point(self, point):
        image = self.imageloader.download(point)
        image = image.crop((150, 150, 200, 200)) #Image 50 x 50
        self.__save(image, "img" + (str(point.latitude) + "_" + str(point.longitude)+".png"))

    def generate(self, bbox):
        imageLoader = ImageLoader()
        images = imageLoader.downloadImagesByPositions(bbox)

        numRows = len(images)
        numCols = len(images[0])

        for i in range(0, numRows):
            for j in range(0, numCols):
                for x in range(0, 10):
                    for y in range(0, 10):
                        img = images[i][j].getImage().crop((x * 32, y * 32, (x + 1) * 32, (y + 1) * 32))
                        self.__save(img, (str(images[i][j].getPosition().latitude) + "_" + str(x) + str(y) + "_" + str(images[i][j].getPosition().longitude)+".jpg"))




    def __save(self, image, filename):
        filepath = self.destinationPath + filename
        self.__removeIfExists(filepath)
        image.save(filepath)

    def __removeIfExists(self, filepath):
        if(os.path.exists(filepath)):
            os.remove(filepath)
