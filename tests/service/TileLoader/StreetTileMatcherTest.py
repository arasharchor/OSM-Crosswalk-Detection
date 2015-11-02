from src.data.StreetTileMatcher import StreetTileMatcher
from src.base.Bbox import Bbox
from src.service.StreetLoader.StreetLoader import StreetLoader
import unittest


class StreetTileMatcherTest(unittest.TestCase):

    def test_constructor(self):
        bbox = self.getBbox()
        streets = self.load_streets(bbox)
        matcher = StreetTileMatcher.from_default(streets, bbox)
        self.assertEquals(len(matcher.used_tiles), 170)
        self.assertEquals(len(matcher.streets), len(streets))

    def test_streetdownload(self):
        bbox = self.getBbox()
        streets = self.load_streets(bbox)
        self.assertTrue(len(streets) > 80)

    def test_exclude_lake_tiles(self):
        bbox = self.getBbox()
        streets = self.load_streets(bbox)
        matcher = StreetTileMatcher.from_default(streets, bbox)
        matcher.match()
        self.assertEquals(matcher.used_tiles[(matcher.tminy,matcher.tminx)], False)

    def load_streets(self,bbox):
        loader = StreetLoader()
        return loader.getStreets(bbox)

    def getBbox(self):
        #Bbox with streets and a lot of lake
        return Bbox(8.822586, 47.217358, 8.833453, 47.221799)