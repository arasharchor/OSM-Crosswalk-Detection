from src.detection.BoxWalker import BoxWalker
from src.base.Bbox import Bbox
from src.base.TileDrawer import TileDrawer

'''
This example visualizes the results of the boxwalker
'''


def Rappi():
    return Bbox.from_lbrt(8.814650, 47.222553, 8.820035, 47.225935)

def Luzern():
    return Bbox.from_lbrt(8.301307, 47.046349, 8.305528, 47.051053)

def BernAltStadt():
    #TrainSet
    return Bbox.from_lbrt(7.444389, 46.947913, 7.448316, 46.949693)

def ChurBhfAltstadt():
    #TrainSet
    return Bbox.from_lbrt(9.528281, 46.850342, 9.532599, 46.853980)

def Zurich2():
    #Trainset
    return Bbox.from_lbrt(8.530470, 47.366188, 8.537807, 47.372053)

def BernKoeniz():
    return Bbox.from_lbrt(7.406960, 46.920077, 7.415008, 46.924285)

def Lausanne():
    return Bbox.from_lbrt(6.555186, 46.508591, 6.563499, 46.516437)

def Lyss():
    #Trainset
    return Bbox.from_lbrt(7.304337, 47.072818, 7.308200, 47.075229)

def zh1():
    return Bbox.from_lbrt(8.522537, 47.375915, 8.526331, 47.376639)

def zh_schlieren_test():
    return Bbox.from_lbrt(8.441207, 47.394649, 8.449643, 47.399710)

def zh_hardbrucke_test():
    return Bbox.from_lbrt(8.517822, 47.386440, 8.520540, 47.388008)

def zh_hardbrucke_test2():
    return Bbox.from_lbrt(8.521436, 47.390424, 8.524241, 47.391289)

def zh_quartier1():
    return Bbox.from_lbrt(8.528067, 47.393102, 8.532648, 47.394939)

def zh_europabrucke():
    return Bbox.from_lbrt(8.492554, 47.391842, 8.503230, 47.394553)

def winti1():
    return Bbox.from_lbrt(8.716155, 47.511909, 8.721038, 47.515722)

def winti_innenstadt():
    return Bbox.from_lbrt(8.723835, 47.497560, 8.733661, 47.501156)

def thun_innenstadt():
    return Bbox.from_lbrt(7.624835, 46.758937, 7.630741, 46.762592)

def heiligkreuz():
    return Bbox.from_lbrt(9.408957, 47.055055, 9.418505, 47.060288)

def staefa():
    return Bbox.from_lbrt(8.729157, 47.233379, 8.741170, 47.238049)

def zh_buchs():
    return  Bbox.from_lbrt(8.432206, 47.456906, 8.441375, 47.461262)

def ag_baden():
    return Bbox.from_lbrt(8.308925, 47.464633, 8.317642, 47.467798)

def ag_baden2():
    return Bbox.from_lbrt( 8.314834, 47.462698, 8.324612, 47.468880)

def zh_frauental_quartier():
    return Bbox.from_lbrt(8.507748, 47.355263, 8.510934, 47.358226)

def zh_quartier2():
    return Bbox.from_lbrt(8.520495, 47.369944, 8.523971, 47.372846)

def RappiUhuereGross():
    return Bbox.from_lbrt(8.804742, 47.215446, 8.850833, 47.237799)

def ZurichUhuereGrossHalb():
    return Bbox.from_lbrt(8.523379, 47.368823, 8.543379, 47.380823)

def ZurichUhuereGross():
    return Bbox.from_lbrt(8.523379, 47.368823, 8.553379, 47.390823)

def ZurichUhuereGross2():
    return Bbox.from_lbrt(8.523379, 47.368823, 8.573379, 47.390823)

def ZurichUhuereGross3():
    return Bbox.from_bltr(47.372759, 8.473965, 47.399972, 8.510429)

def Zug_sz():
    return Bbox.from_bltr(47.171100, 8.511467, 47.173771, 8.519041)

def zh_zollikon_test_gross():
    return Bbox.from_bltr(47.355633, 8.543026, 47.372811, 8.570957)

def zh_kilchberg():
    return Bbox.from_bltr(47.320074, 8.547435, 47.323934, 8.550514)


#Start of the real function

bbox = zh_zollikon_test_gross()

# Let's analyzer the bbox
walker = BoxWalker(bbox)
walker.load_convnet()
walker.load_tiles()
walker.load_streets()

walker.walk()
crosswalkNodes = walker.plain_result # Get all results and don't compare with osm crosswalks

# Draw the crosswalks on the tile and show us the result
drawer = TileDrawer.from_tile(walker.tile)
for node in crosswalkNodes:
    drawer.draw_point(node)
drawer.drawsection.save("boxsave.jpg")
drawer.drawsection.show()

