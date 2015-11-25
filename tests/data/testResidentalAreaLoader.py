import unittest
from src.data.ResidentalAreaLoader import ResidentalAreaLoader
from src.base.Bbox import Bbox
from src.detection.BoxWalker import BoxWalker
from src.base.TileDrawer import TileDrawer
from src.base.Node import Node

class TestStreetLoader(unittest.TestCase):

    def test_show_residentials(self):
        bbox = Bbox.from_bltr(47.115242, 9.299165, 47.130591, 9.335707)
        loader = ResidentalAreaLoader()
        residentials = loader.load(bbox)
        self.assertGreater(len(residentials), 0)
        for i in range(len(residentials)):
            residentials[i] = residentials[i].extend(100)
        tile = self.load_tiles(bbox)
        drawer = self.draw(tile, residentials)
        drawer.show()

    def test_in_area(self):
        node = Node(47.124956, 9.309148)
        bbox = Bbox.from_bltr(47.115242, 9.299165, 47.130591, 9.335707)
        loader = ResidentalAreaLoader()
        residentials = loader.load(bbox)
        true_count = 0
        for area in residentials:
            if area.in_area(node):
                true_count += 1
        self.assertEquals(true_count, 1)

    def test_not_in_area(self):
        bhf = Node(47.119996, 9.312480)
        bbox = Bbox.from_bltr(47.115242, 9.299165, 47.130591, 9.335707)
        loader = ResidentalAreaLoader()
        residentials = loader.load(bbox)
        true_count = 0
        for area in residentials:
            if area.in_area(bhf):
                true_count += 1
        self.assertEquals(true_count, 0)

    def test_offset(self):
        bhf = Node(47.119996, 9.312480)
        bbox = Bbox.from_bltr(47.115242, 9.299165, 47.130591, 9.335707)
        loader = ResidentalAreaLoader()
        residentials = loader.load(bbox)
        true_count = 0
        for area in residentials:
            if area.in_area(bhf, 100):
                true_count += 1
        self.assertEquals(true_count, 1)

    def test_poly_to_nodes(self):
        bbox = Bbox.from_bltr(47.115242, 9.299165, 47.130591, 9.335707)
        loader = ResidentalAreaLoader()
        residentials = loader.load(bbox)
        area = residentials[0]

        nodes = area._to_nodes(area.polygon)

        for i in range(len(nodes)):
            distance = nodes[i].get_distance_in_meter(area.nodes[i])
            self.assertEquals(distance, 0)



    def load_tiles(self, bbox):
        boxwalker = BoxWalker(bbox)
        boxwalker.load_tiles()
        return boxwalker.tile

    def draw(self, tile, residentials):
        drawer = TileDrawer.from_tile(tile)
        for area in residentials:
            for i in range(len(area.nodes) -1):
                drawer.draw_line(area.nodes[i], area.nodes[i+1], 30)
                drawer.draw_point(area.nodes[i])

        return drawer


    def ZurichBellvue(self):
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)