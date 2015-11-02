import httplib2
from StringIO import StringIO
from PIL import Image
from src.base.Tile import Tile
from src.base.Bbox19 import Bbox19
from src.service.TilesLoader.MultiLoader import MultiLoader


class TileLoader:
    # http://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/
    # ?mapArea=47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977
    # &key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq

    def __init__(self):
        self.PRELINK = "http://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea="
        self.POSTLINK = "&key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq"
        self.printStat = True
        self.lastStat = 0

    def generate_link(self, bbox):
        url = self.PRELINK + bbox.getBingFormat() + self.POSTLINK
        return url


    def download19(self,bbox):
        result = []
        bboxes19 = Bbox19.toBbox19(bbox)

        urls = []
        for y in range(len(bboxes19)):
            for x in range(len(bboxes19[y])):
                box = bboxes19[y][x]
                url = self.generate_link(box)
                urls.append(url)

        loader = MultiLoader.from_url_list(urls)
        loader.download()

        i = 0
        for y in range(len(bboxes19)):
            result.append([])
            for x in range(len(bboxes19[y])):
                box = bboxes19[y][x]
                img = loader.results[i]
                tile = Tile(img, box)
                result[y].append(tile)
                i += 1

        return result

