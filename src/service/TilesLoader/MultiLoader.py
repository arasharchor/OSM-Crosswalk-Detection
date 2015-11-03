from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import StringIO
from PIL import Image

class MultiLoader:
    def __init__(self):
        self.urls = []
        self.results = []

    @classmethod
    def from_url_list(cls, urls):
        loader = cls()
        loader.urls = urls
        return loader

    def download(self):
        results = []
        tile_per_trial = 40
        nb_urls = len(self.urls)

        for i in range(int(nb_urls/tile_per_trial)):
            start = i * tile_per_trial
            end = start + tile_per_trial
            if(end >= nb_urls): end = nb_urls -1
            urlpart = self.urls[start:end]
            result = self._download(urlpart)
            results += result

        self.results = self._convert_to_image(results)

    def _download(self, urls):
        pool = ThreadPool(10)
        results = pool.map(urllib2.urlopen, urls)
        pool.close()
        pool.join()
        return results


    def _convert_to_image(self, results):
        ret = []
        for loads in results:
            img = loads.read()
            img = Image.open(StringIO.StringIO(img))
            ret.append(img)

        return ret