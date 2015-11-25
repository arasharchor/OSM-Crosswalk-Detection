from src.base.Street import Street
from src.base.Node import Node
from src.base.ResidentalArea import ResidentalArea
import httplib2
from xml.etree import ElementTree

class ResidentalAreaLoader:
    def __init__(self, developerKey = "YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"):
        self.developerKey = developerKey
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[landuse=residential][bbox="
        self.__LINK_POSTFIX = "]?key="
        self._nodemap = None

    def request(self, box):
        postfix = self.to_mapquest_format(box) + self.__LINK_POSTFIX + self.developerKey
        url = self.__LINK_PREFIX + postfix
        print url
        resp, content = httplib2.Http().request(url)
        return ElementTree.fromstring(content)

    def to_mapquest_format(self, bbox):
        return str(bbox.left) + "," + str(bbox.bottom) + "," + str(bbox.right) + "," + str(bbox.top)

    def load(self, bbox):
        residentals = self._load_residentals(bbox)
        return residentals


    def _load_residentals(self, bbox):
        tree = self.request(bbox)
        self._nodemap = self._get_node_map(tree)
        return self._parse_bbox(tree)


    def _parse_bbox(self, tree):
        areas = []
        for way in tree.iter("way"):
            area = self._parse_way(way)
            areas.append(area)
        return areas


    def _parse_way(self, way):
        nodes = []
        for nd in way.iter("nd"):
            nd_id = nd.get("ref")
            node = self._nodemap[nd_id]
            nodes.append(node)

        area = ResidentalArea.from_nodes(nodes)
        return area


    def _filter_crosswalks(self, tree):
        for node in tree.iter('node'):
            for tag in node.iter('tag'):
                if self._is_crosswalk(tag):
                    self.crosswalks.append(Node(node.get('lat'), node.get('lon')))

    def _parse_tree(self, tree):
        node_map = self._get_node_map(tree)
        for way in tree.iter('way'):
            for tag in way.iter('tag'):
                for category in self._STREET_CATEGORIES:
                    if self._is_in_category(tag,category):
                        results = self._parse_way(way, node_map)
                        self.streets += results

    def _is_in_category(self,tag, category):
        return str(tag.attrib) == "{'k': 'highway', 'v': '" + category + "'}"

    def _is_crosswalk(self, tag):
        return str(tag.attrib) == "{'k': 'highway', 'v': 'crossing'}"



    def _create_street(self, way):
        ident = way.get('id')
        name = ""
        highway = ""

        for tag in way.iter('tag'):
            if tag.attrib['k'] == 'name':
                name = tag.attrib['v']
            if tag.attrib['k'] == 'highway':
                highway = tag.attrib['v']

        street = Street.from_info(name,ident,highway)
        return street

    def _create_node_list(self, way, node_map):
        nodes = []
        for node in way.iter('nd'):
            nid = node.get('ref')
            if nid in node_map:
                nodes.append(node_map[nid])
        return nodes

    def _get_node_map(self,tree):
        nodes = {}
        for node in tree.iter('node'):
            nodes[node.get('id')] = Node(node.get('lat'), node.get('lon'), node.get('id'))
        return nodes