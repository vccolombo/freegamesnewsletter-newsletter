import json
import os
import shutil
import logging

class Game:
    DATA_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'

    def __init__(self, name, url, store, is_free_to_keep):
        self.name = name
        self.url = url
        self.store = store
        self.is_free_to_keep = is_free_to_keep
    
    @staticmethod
    def save_todays_free_games(list_of_games):
        Game._save_yesterdays_free_games()

        file_path = Game.DATA_DIR_PATH + 'today_games.json'
        dict_of_games = Game.make_dict_of_games(list_of_games)
        with open(file_path, 'w') as f:
            json.dump(dict_of_games, f)

    @staticmethod
    def _save_yesterdays_free_games():
        file_path_today = Game.DATA_DIR_PATH + 'today_games.json'
        file_path_yesterday = Game.DATA_DIR_PATH + 'yesterday_games.json'

        try:
            shutil.copy2(file_path_today, file_path_yesterday)
        except shutil.Error as err:
            logging.error("COULDN'T SAVE YESTERDAY'S GAMES: " + err)
        except FileNotFoundError as err:
            logging.error("COULDN'T SAVE YESTERDAY'S GAMES: " + str(err))

    @staticmethod
    def make_dict_of_games(list_of_games):
        dict_of_games = {}
        for game in list_of_games:
            dict_of_games[game.name] = {
                'name': game.name,
                'url': game.url,
                'store': game.store,
                'is_free_to_keep': game.is_free_to_keep
            }
        
        return dict_of_games
    
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
        list_of_games = []

        try:
            with open(file_path) as f:
                for game in json.load(f).values():
                    list_of_games.append(Game(game['name'], game['url'], game['store'], game['is_free_to_keep']))
        except FileNotFoundError as err:
            logging.error("COULDN'T LOAD GAMES FROM FILE: " + str(err))

        return list_of_games