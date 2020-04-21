import json
import os
import logging

class Game:
    DATA_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/crawlers/data/'

    logger = logging.getLogger(__name__)

    def __init__(self, name, url, image, description):
        self.name = name
        self.url = url
        self.image = image
        self.description = description
    
    @staticmethod
    def get_today_free_games():
        file_path = Game.DATA_DIR_PATH + 'today_games.json'
        return Game._get_games_from_file(file_path)
    
    @staticmethod
    def get_yesterday_free_games():
        file_path = Game.DATA_DIR_PATH + 'yesterday_games.json'
        return Game._get_games_from_file(file_path)
    
    @staticmethod
    def _get_games_from_file(file_path):
        games = []

        try:
            f = open(file_path)
            games_json = json.load(f)
            for game in games_json:
                new_game = Game(game['name'], game['url'], game['image'], game['description'])
                games.append(new_game)
        except FileNotFoundError as err:
            Game.logger.warn("COULD NOT LOAD GAMES FROM FILE: " + str(err))
        except Exception as err:
            Game.logger.error(str(err))

        return games