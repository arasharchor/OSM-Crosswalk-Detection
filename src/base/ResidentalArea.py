import Polygon, Polygon.IO
from src.base.Node import Node
from src.base.Bbox import Bbox
#https://bitbucket.org/jraedler/polygon2/src/9917e23dc99aad8ae4fd8229ef4c27961bccae4a/doc/?at=master
class ResidentalArea:
    def __init__(self):
        self.nodes = []
        self.polygon = None

    @classmethod
    def from_nodes(cls, nodes):
        area = cls()
        area.nodes = nodes
        area.polygon = area._to_polygon(nodes)
        return area

    def _to_polygon(self, nodes):
        poly = []
        for nd in nodes:
            point = (nd.latitude, nd.longitude)
            poly.append(point)
        return Polygon.Polygon(poly)

    def _to_nodes(self, poly):
        nodes = []
        points = poly.contour(0)
        for p in points:
            n = Node(p[0], p[1])
            nodes.append(n)
        return nodes

    def in_area(self, node, meter_offset=0):
        if(meter_offset==0):
            (x,y) = (node.latitude, node.longitude)
            return self.polygon.isInside(x,y)
        else:
            offset_area = self.extend(meter_offset)
            return offset_area.in_area(node)

    def extend(self, meter):
        poly = self._to_polygon(self.nodes)
        (x_scale, y_scale) = self._get_scale_factors(meter)
        poly.scale(x_scale, y_scale)
        nodes = self._to_nodes(poly)
        return ResidentalArea.from_nodes(nodes)

    def _get_scale_factors(self, extend_meter):
        bbox = self.to_bbox()
        x_distance = bbox.get_x_distance()
        y_distance = bbox.get_y_distance()

        x = (x_distance + extend_meter)/ x_distance
        y = (y_distance + extend_meter) / y_distance
        return (x,y)

    def to_bbox(self):
        poly = self._to_polygon(self.nodes)
        box = poly.boundingBox()
        return Bbox.from_bltr(box[0], box[2], box[1], box[3])

