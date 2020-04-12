import json
import os

class Game:
    games_file_path = os.path.dirname(os.path.abspath(__file__)) + '/data/free_games.json'

    def __init__(self, name, url, store):
        self.name = name
        self.url = url
        self.store = store
    
    @staticmethod
    def write_games_to_file(list_of_games):
        dict_of_games = Game.make_dict_of_games(list_of_games)
        with open(Game.games_file_path, 'w') as f:
            json.dump(dict_of_games, f)

    @staticmethod
    def make_dict_of_games(list_of_games):
        dict_of_games = {}
        for game in list_of_games:
            dict_of_games[game.name] = {
                'name': game.name,
                'url': game.url,
                'store': game.store
            }
        
        return dict_of_games
    
    @staticmethod
    def get_games():
        list_of_games = []

        with open(Game.games_file_path) as f:
            for game in json.load(f).values():
                list_of_games.append(Game(game['name'], game['url'], game['store']))

        return list_of_games