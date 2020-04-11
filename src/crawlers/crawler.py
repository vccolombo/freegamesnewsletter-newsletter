import scrapy
from scrapy.crawler import CrawlerProcess

from .steamdb.steamdb_spider import SteamdbSpider

class Crawler:
    configs = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1
    }

    def run(self):
        self.crawl_steamdb()

    def crawl_steamdb(self):
        process = CrawlerProcess(self.configs)

        process.crawl(SteamdbSpider)
        process.start()