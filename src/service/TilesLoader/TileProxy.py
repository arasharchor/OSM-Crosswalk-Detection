from src.service.TilesLoader.TileLoader import TileLoader
from src.base.Tile import Tile
from src.base.Bbox import Bbox
from PIL import Image
from geopy import Point
import pickle


class TileProxy:
    def __init__(self, bbox):
        self.bbox = bbox
        loader = TileLoader()
        print "start loading"
        self.tiles = loader.download19(self.bbox)
        print "finish loading"

    def getTileByPoint(self, point):
        if(not self.bbox.inBbox(point)): raise Exception("Point not in bbox")

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                tile = self.tiles[y][x]
                if(tile.bbox.inBbox(point)):
                    return tile
        raise Exception("No tile found. Programm error! Call Severin Buehler")

    def getTileIndexes(self, point):
        if(not self.bbox.inBbox(point)): raise Exception("Point not in bbox")
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                tile = self.tiles[y][x]
                if(tile.bbox.inBbox(point)):
                    return (y,x)


    def getBigTile(self, point1, point2):
        box = Bbox()
        box.set(point1, point2)

        tileId1 = self.getTileIndexes(box.getDownLeftPoint())
        tileId2 = self.getTileIndexes(box.getUpRightPoint())

        image = self.mergeImage(tileId1,tileId2)

        firstTile = self.tiles[tileId1[0]][tileId1[1]]
        lastTile = self.tiles[tileId2[0]][tileId2[1]]

        bbox = Bbox(firstTile.bbox.left, firstTile.bbox.bottom, lastTile.bbox.right, lastTile.bbox.top)
        return Tile(image, bbox)

    def getBigTile2(self):
        return self.getBigTile(self.bbox.getDownLeftPoint(),self.bbox.getUpRightPoint())

    def getBigTileByNodes(self, node1, node2):
        assert self.bbox.inBbox(node1.toPoint()) and self.bbox.inBbox(node2.toPoint())

        point1 = self.__getLeftDownPoint(node1, node2)
        point2 = self.__getUpRightPoint(node1, node2)

        assert self.bbox.inBbox(point1) and self.bbox.inBbox(point2)

        return self.getBigTile(point1, point2)

    def mergeImage(self, tileId1, tileId2):
        yCount = tileId2[0] - tileId1[0] + 1
        xCount = tileId2[1] - tileId1[1] + 1
        width, height = self.tiles[0][0].image.size

        result = Image.new("RGBA", (xCount * width, yCount * height))

        for y in range(yCount):
            for x in range(xCount):
                tiley = tileId1[0] + y
                tilex = tileId1[1] + x
                t = self.tiles[tiley][tilex].image
                result.paste(t, (x * width, (yCount - y - 1) * height))

        return result

    def __getLeftDownPoint(self, node1, node2):
        lat1 = node1.lat
        lat2 = node2.lat
        lon1 = node1.lon
        lon2 = node2.lon

        if(lat2 < lat1):
            #Swap
            temp = lat1
            lat1 = lat2
            lat2 = temp

        if(lon2 < lon1):
            #Swap
            temp = lon1
            lon1 = lon2
            lon2 = temp

        return Point(lat1, lon1)

    def __getUpRightPoint(self,node1, node2):
        lat1 = node1.lat
        lat2 = node2.lat
        lon1 = node1.lon
        lon2 = node2.lon

        if(lat2 < lat1):
            #Swap
            temp = lat1
            lat1 = lat2
            lat2 = temp

        if(lon2 < lon1):
            #Swap
            temp = lon1
            lon1 = lat2
            lon2 = temp

        return Point(lat2,lon2)


    def getTiles(self):
        return self.tiles



    def toFile(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def fromFile(filepath):
        with open(filepath, 'rb') as f:
            proxy = pickle.load(f)
            return proxy