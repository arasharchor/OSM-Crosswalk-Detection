from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import StringIO
from PIL import Image
from fake_useragent import UserAgent

class MultiLoader:
    def __init__(self):
        self.urls = []
        self.results = []
        self.useragent = UserAgent()


    @classmethod
    def from_url_list(cls, urls):
        loader = cls()
        loader.urls = urls
        return loader

    def generate_request(self, url):
        header = {'User-Agent': self.useragent.random}
        req = urllib2.Request(url, headers=header)
        return req

    def download(self):
        requests = []
        for url in self.urls:
            req = self.generate_request(url)
            requests.append((req))
        # Make the Pool of workers
        pool = ThreadPool(10)
        # Open the urls in their own threads
        # and return the results
        results = pool.map(urllib2.urlopen, requests)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()

        self.results = self._convert_to_image(results)

    def _convert_to_image(self, results):
        ret = []
        for loads in results:
            img = loads.read()
            img = Image.open(StringIO.StringIO(img))
            ret.append(img)

        return ret