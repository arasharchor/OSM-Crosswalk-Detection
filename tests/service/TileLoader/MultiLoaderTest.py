import unittest
from src.service.TilesLoader.MultiLoader import MultiLoader

class TestMultiLoader(unittest.TestCase):
    def test_download(self):
        urls = ["http://www.kerry-beaches.com/images/contact-me-facebook-thumbnail.jpeg", "http://www.fsb.org.uk/092/images/twitter-logo.jpg", "http://vignette4.wikia.nocookie.net/trekcreative/images/7/78/Galaxy_Map-Huge.jpg/revision/latest?cb=20091230105332"]
        loader = MultiLoader.from_url_list(urls)
        loader.download()
        self.assertEquals(3, len(loader.results))
        img1 = loader.results[0]
        self.assertEquals(256, img1.size[0])
        img2 = loader.results[1]
        self.assertEquals(300, img2.size[0])
        img3 = loader.results[2]
        self.assertEquals(5600, img3.size[0])
