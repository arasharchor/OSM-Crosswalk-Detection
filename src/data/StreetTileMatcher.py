from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
class StreetTileMatcher:
    def __init__(self):
        self.streets = None
        self.used_tiles = {}
        self.tiles_bbox = {}
        self.tmaxx = None
        self.tmaxy = None
        self.tminx = None
        self.tminy = None

    @classmethod
    def from_default(cls, streets, bbox):
        matcher = cls()
        matcher.streets = streets
        matcher._calc_Tilenumber(bbox)
        matcher._calc_Tile_bbox()
        return matcher

    def _calc_Tilenumber(self, bbox):
        mercator = GlobalMercator()
        mminx, mminy = mercator.LatLonToMeters(float(bbox.bottom), float(bbox.left))
        mmaxx, mmaxy = mercator.LatLonToMeters(float(bbox.top), float(bbox.right))
        self.tmaxx, self.tmaxy = mercator.MetersToTile( mmaxx, mmaxy, Constants.ZOOM)
        self.tminx, self.tminy = mercator.MetersToTile( mminx, mminy, Constants.ZOOM)
        for ty in range(self.tminy, self.tmaxy+1):
            for tx in range(self.tminx, self.tmaxx+1):
                self.used_tiles[(ty,tx)] = True

    def _calc_Tile_bbox(self):
        mercator = GlobalMercator()
        for key in self.used_tiles:
            (ty,tx) = key
            bbox = mercator.TileLatLonBounds(tx,ty,Constants.ZOOM)
            self.tiles_bbox[key] = bbox


    def match(self):
        for street in self.streets:
            n1 = street.nodes[0]
            n2 = street.nodes[1]
            self._match_nodes(n1,n2)

