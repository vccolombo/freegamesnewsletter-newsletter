import scrapy

from game import Game

class SteamdbSpider(scrapy.Spider):
    name = 'steamdb'
    steam_url = 'https://store.steampowered.com'

    def start_requests(self):
        start_urls = ['https://steamdb.info/sales/?min_discount=95&min_rating=0']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        games_on_sale = self._get_list_of_games_on_sale(response)
        free_games = self._get_free_games(games_on_sale)
        Game.save_todays_free_games(free_games)

    def _get_list_of_games_on_sale(self, response):
        sales_section = response.css('div.sales-section')
        sales_table = sales_section.css('table.table-sales')
        sales_tbody = sales_table.css('tbody')
        sales_games = sales_tbody.css('tr')

        list_of_games_on_sale = []
        for game in sales_games:
            new_game = self._make_game(game)
            list_of_games_on_sale.append(new_game)

        return list_of_games_on_sale

    def _get_free_games(self, games):
        free_games = []
        for game in games:
            if game.is_free_to_keep:
                free_games.append(game)

        return free_games

    def _make_game(self, game):
        game_name = game.css('a.b::text').get()
        game_url = self.steam_url + game.css('a.b::attr(href)').get()
        game_is_free_to_keep = len(game.css('span.sales-free-to-keep')) > 0

        return Game(game_name, game_url, "Steam", game_is_free_to_keep)