import scrapy

from game import Game

class SteamdbSpider(scrapy.Spider):
    name = 'steamdb'
    steam_url = 'https://store.steampowered.com'

    def start_requests(self):
        start_urls = ['https://steamdb.info/sales/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        games_on_sale = self.get_list_of_games_on_sale(response)
        free_games = self.get_free_games(games_on_sale)
        Game.write_games_to_file(free_games)

    def get_list_of_games_on_sale(self, response):
        sales_section = response.css('div.sales-section')
        sales_table = sales_section.css('table.table-sales')
        sales_tbody = sales_table.css('tbody')
        sales_games = sales_tbody.css('tr')
        return sales_games

    def get_free_games(self, games):
        free_games = []
        for game in games:
            if self.is_game_free(game):
                new_free_game = self.make_game(game)
                free_games.append(new_free_game)

        return free_games

    def is_game_free(self, game):
        if len(game.css('span.sales-free-to-keep')) > 0:
            return True
        else:
            return False

    def make_game(self, game):
        game_name = game.css('a.b::text').get()
        game_url = self.steam_url + game.css('a.b::attr(href)').get()

        return Game(game_name, game_url, "Steam")