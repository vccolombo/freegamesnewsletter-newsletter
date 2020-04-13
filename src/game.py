import json
import os

class Game:
    free_games_file_path = os.path.dirname(os.path.abspath(__file__)) + '/data/free_games.json'

    def __init__(self, name, url, store, is_free_to_keep):
        self.name = name
        self.url = url
        self.store = store
        self.is_free_to_keep = is_free_to_keep
    
    @staticmethod
    def write_games_to_file(list_of_games):
        dict_of_games = Game.make_dict_of_games(list_of_games)
        with open(Game.free_games_file_path, 'w') as f:
            json.dump(dict_of_games, f)

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
    def get_todays_free_games():
        list_of_games = []

        with open(Game.free_games_file_path) as f:
            for game in json.load(f).values():
                list_of_games.append(Game(game['name'], game['url'], game['store'], game['is_free_to_keep']))

        return list_of_games