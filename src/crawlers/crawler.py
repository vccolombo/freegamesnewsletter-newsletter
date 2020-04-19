import scrapy
from scrapy.crawler import CrawlerProcess
import os
import shutil
import logging

from .steam import spider as steam

class Crawler:
    DATA_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'
    CONFIGS = {
        'FEED_FORMAT': 'json',
        'FEED_URI': DATA_DIR_PATH + 'today_games.json'
    }

    def run_newsletter(self):
        self._save_yesterday_results()
        self._run()

    def _save_yesterday_results(self):
        src = self.DATA_DIR_PATH + 'today_games.json'
        dst = self.DATA_DIR_PATH + 'yesterday_games.json'
        try:
            shutil.move(src, dst)
        except FileNotFoundError as err:
            logging.warn('COULD NOT SAVE YESTERDAY GAMES: ' + str(err))

    def _run(self):
        self._crawl_steam()

    def _crawl_steam(self):
        process = CrawlerProcess(self.CONFIGS)
        process.crawl(steam.Spider)
        process.start()