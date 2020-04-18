import scrapy
from scrapy.crawler import CrawlerProcess
import os

from .steam import spider as steam

class Crawler:
    DATA_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'
    configs = {
        'FEED_FORMAT': 'json',
        'FEED_URI': DATA_DIR_PATH + 'test.json'
    }

    def run(self):
        self._crawl_steam()

    def _crawl_steam(self):
        process = CrawlerProcess(self.configs)
        process.crawl(steam.Spider)
        process.start()