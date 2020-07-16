from datetime import datetime
import calendar
import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup

from game import Game
from .broker import EmailBroker

class MailSender:
    TEMPLATES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/templates/'

    logger = logging.getLogger(__name__)

    site_url = os.environ["SITE_URL"]

    def __init__(self):
        jinja_env = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.html_template = jinja_env.get_template('newsletter.html')

        self.broker = EmailBroker()

    def send(self, contact_list):
        games_to_send = self._get_games_to_send()
        subject = self._generate_subject()
        if games_to_send:
            self.logger.info(f"Sending {len(games_to_send)} games...")
            self.broker.connect()
            for receiver in contact_list:
                msg = self._generate_message(receiver, games_to_send)
                self._publish_email(receiver, subject, msg)
            self.broker.close()
        else:
            self.logger.info("No games to send today")

    def _get_games_to_send(self):
        today_games = Game.get_today_free_games()
        yesterday_games = Game.get_yesterday_free_games()

        games_to_send = []
        for game in today_games:
            if not self._game_was_sent_yesterday(game, yesterday_games):
                games_to_send.append(game)

        return games_to_send

    def _game_was_sent_yesterday(self, game, yesterday_games):
        return any(game.name == yesterday_game.name for yesterday_game in yesterday_games)

    def _generate_message(self, receiver, games_list):
        return self._generate_html_message(games_list, receiver)
    
    def _generate_subject(self):
        today = datetime.now()
        day = str(today.day)
        month = calendar.month_abbr[today.month]

        return f"Free-to-keep games {day} {month}"

    def _generate_html_message(self, games_list, subscriber):
        unsubscribe_url = self._get_unsubscribe_url(subscriber)
        html = self.html_template.render(
            games=games_list, unsubscribe_url=unsubscribe_url)
        return html

    def _get_unsubscribe_url(self, subscriber):
        return self.site_url + f"/unsubscribe?email={subscriber.email}&code={subscriber.unsubscribe_code}"

    def _publish_email(self, receiver, subject, message):
        self.broker.publish_email(receiver.email, subject, message)