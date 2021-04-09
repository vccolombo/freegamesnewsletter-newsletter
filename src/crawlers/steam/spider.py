import scrapy
from furl import furl


class Spider(scrapy.Spider):
    name = 'Steam'

    STEAM_URL = 'https://store.steampowered.com'
    COOKIES = {
        'birthtime': '628488001',
        'mature_content': '1',
    }

    def start_requests(self):
        start_url = self.STEAM_URL + '/search/?category1=998&page=1'
        yield scrapy.Request(url=start_url, callback=self._parse_search)

    def _parse_search(self, response):
        all_games = response.xpath(
            '//*[contains(@class, "search_result_row")]')
        for game in all_games:
            if self._is_game_free(game):
                game_url = self._get_game_url(game)
                yield scrapy.Request(url=game_url, callback=self._parse_game, cookies=self.COOKIES)

        next_pages = self._get_urls_to_next_pages(response)
        for next_page in next_pages:
            yield scrapy.Request(url=next_page, callback=self._parse_search)

    def _is_game_free(self, game):
        discount = game.xpath(
            './/div[contains(@class, "search_discount")]/span/text()').get()
        return discount == '-100%'

    def _get_game_url(self, game):
        return game.xpath('./@href').get()

    def _parse_game(self, response):
        name = response.xpath('//div[@class="apphub_AppName"]/text()').get()
        game_url = furl(response.url).remove(args=True).url
        image_url = response.xpath(
            '//img[@class="game_header_image_full"]/@src').get()
        description = response.xpath(
            '//div[@class="game_description_snippet"]/text()').get()
        yield {
            'name': name,
            'url': game_url,
            'image': image_url,
            'description': description.strip()
        }

    def _get_urls_to_next_pages(self, response):
        pagination = response.xpath('//div[@class="search_pagination_right"]')
        links = pagination.xpath(
            './a[not(contains(@class, "pagebtn"))]/@href').getall()
        return links
