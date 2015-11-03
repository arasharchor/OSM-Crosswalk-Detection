import httplib2
from StringIO import StringIO
from PIL import Image
from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
from src.base.Bbox import Bbox
from src.base.Tile import Tile
from src.data.MultiLoader import MultiLoader

class TileLoader:
    def __init__(self, bbox):
        self.bbox = bbox
        self.PRELINK = 'https://t3.ssl.ak.tiles.virtualearth.net/tiles/a'
        self.POSTLINK = '.jpeg?g=4401&n=z'

    def getTiles(self):
        return self._download_tiles(self.bbox)

    def _url_to_image(self, url):
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return image

    def _build_url(self, quadtree):
        return self.PRELINK + str(quadtree) + self.POSTLINK

    def _download_image(self, quadtree):
        url = self._build_url(quadtree)
        return self._url_to_image(url)

    def _download_tiles(self, bbox):
        mercator = GlobalMercator()
        mminx, mminy = mercator.LatLonToMeters(float(bbox.bottom), float(bbox.left))
        mmaxx, mmaxy = mercator.LatLonToMeters(float(bbox.top), float(bbox.right))
        tmaxx, tmaxy = mercator.MetersToTile( mmaxx, mmaxy, Constants.ZOOM)
        tminx, tminy = mercator.MetersToTile( mminx, mminy, Constants.ZOOM)
        urls = []
        row = 0
        for ty in range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):
                #tilefilename = "%s/%s/%s" % (Constants.ZOOM, tx, ty)
                quadtree = mercator.QuadTree(tx, ty, Constants.ZOOM)
                url = self._build_url(quadtree)
                urls.append(url)

        print "- Download", len(urls), "tiles"
        loader = MultiLoader.from_url_list(urls)
        loader.download()

        i = 0
        tiles = []
        row = 0
        for ty in range(tminy, tmaxy+1):
            tiles.append([])
            for tx in range(tminx, tmaxx+1):
                #tilefilename = "%s/%s/%s" % (Constants.ZOOM, tx, ty)

                image = loader.results[i]
                bottom, left, top, right = mercator.TileLatLonBounds(tx, ty, Constants.ZOOM)
                bbox = Bbox(left,bottom,right,top) #(left, bottom, top, right)
                tile = Tile(image, bbox)
                tiles[row].append(tile)
                i += 1
            row += 1
        return tiles

    def get_big_tile(self):
        tiles = self.getTiles()
        numRows = len(tiles)
        numCols = len(tiles[0])
        width, height = tiles[0][0].image.size

        result = Image.new("RGB", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(tiles[y][x].image,(x * width, (numRows -1 -y) * height))

        first = tiles[0][0]
        last = tiles[numRows -1][numCols -1]
        bbox = Bbox()
        bbox.set(first.bbox.getDownLeftPoint(),last.bbox.getUpRightPoint())

        return Tile(result,bbox)