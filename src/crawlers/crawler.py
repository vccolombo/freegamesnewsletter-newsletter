import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import os
import shutil
import logging

from .steam import spider as steam

class Crawler:
    DATA_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'
    CONFIGS = {
        'USER_AGENT': 'freegamesnewsletter-crawler (contact@freegamesnewsletter.tech)',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2,
        'FEED_FORMAT': 'json',
        'FEED_URI': DATA_DIR_PATH + 'today_games.json',
        'LOG_LEVEL': 'INFO',
        # 'HTTPCACHE_ENABLED': True
    }

    logger = logging.getLogger(__name__)

    def run_newsletter(self):
        self._save_yesterday_results()
        self._run()

    def _save_yesterday_results(self):
        src = self.DATA_DIR_PATH + 'today_games.json'
        dst = self.DATA_DIR_PATH + 'yesterday_games.json'
        try:
            shutil.move(src, dst)
        except FileNotFoundError as err:
            Crawler.logger.warn('COULD NOT SAVE YESTERDAY GAMES: ' + str(err))

    def _run(self):
        self._crawl_steam()

    def _crawl_steam(self):
        runner = CrawlerRunner(Crawler.CONFIGS)
        d = runner.crawl(steam.Spider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run() # the script will block here until the crawling is finished