from src.base.Tile import Tile
import Image, ImageDraw
class TileDrawer:
    def __init__(self):
        self.tile = None
        self.drawsection = None
        self.drawer = None

    @classmethod
    def from_tile(cls, tile):
        drawer = cls()
        drawer.tile = tile
        drawer.drawsection = tile.image
        drawer.drawer = ImageDraw.Draw(drawer.drawsection)
        return drawer

    def draw_point(self, node):
        pointsize = 6
        (x, y) = self.tile.getPixel(node)
        self.drawer.ellipse((x-pointsize, y-pointsize, x+pointsize, y+pointsize), outline=(0,255,0), fill=(0,255,0))

    def draw_line(self, node1, node2):
        pixels1 = self.tile.getPixel(node1)
        pixels2 = self.tile.getPixel(node2)
        self.drawer.line([pixels1,pixels2])