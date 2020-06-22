import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import calendar
import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup

from game import Game

class MailSender:
    TEMPLATES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/templates/'

    logger = logging.getLogger(__name__)

    sender_email = "freegamesnewsletter@gmail.com"
    sender_password = os.environ["FREEGAMESNEWSLETTER_PASSWORD"]

    # smtp configs
    smtp_domain = "smtp.gmail.com"
    smtp_port = 465

    site_url = "https://www.freegamesnewsletter.tech"

    def __init__(self):
        jinja_env = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.html_template = jinja_env.get_template('newsletter.html')

    def send(self, contact_list):
        smtp_client = self._create_smtp_connection()
        
        games_to_send = self._get_games_to_send()
        if games_to_send:
            MailSender.logger.info(f"Sending {len(games_to_send)} games...")
            for receiver in contact_list:
                message = self._generate_message(receiver, games_to_send)
                self._send_mail(receiver, message, smtp_client)
        else:
            MailSender.logger.info("No games to send today")
            
        smtp_client.quit()

    def _create_smtp_connection(self):
        context = ssl.create_default_context()
        smtp_client = smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, context=context)
        smtp_client.login(self.sender_email, self.sender_password)
        return smtp_client

    def _get_games_to_send(self):
        today_games = Game.get_today_free_games()
        yesterday_games = Game.get_yesterday_free_games()

        games_to_email = []
        for game in today_games:
            if not self._game_was_sent_yesterday(game, yesterday_games):
                games_to_email.append(game)

        return games_to_email

    def _game_was_sent_yesterday(self, game, yesterday_games):
        return any(game.name == yesterday_game.name for yesterday_game in yesterday_games)

    def _generate_message(self, receiver, games_list):
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = receiver.email
        message["Subject"] = self._generate_subject()
        message["X-Priority"] = "3"

        html_msg = self._generate_html_message(games_list, receiver)
        text_msg = self._generate_text_message_from_html(html_msg)

        message.attach(MIMEText(text_msg, "plain"))
        message.attach(MIMEText(html_msg, "html"))

        return message
    
    def _generate_subject(self):
        today = datetime.now()
        day = str(today.day)
        month = calendar.month_abbr[today.month]

        return f"Free-to-keep games {day} {month}"

    def _generate_text_message_from_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text()
        return text

    def _generate_html_message(self, games_list, subscriber):
        unsubscribe_url = self._get_unsubscribe_url(subscriber)
        html = self.html_template.render(games=games_list, unsubscribe_url=unsubscribe_url)
        return html

    def _get_unsubscribe_url(self, subscriber):
        return self.site_url + f"/unsubscribe?email={subscriber.email}&code={subscriber.unsubscribe_code}"

    def _send_mail(self, receiver, message, smtp_client):
        receiver_email = receiver.email
        smtp_client.sendmail(self.sender_email, receiver_email, message.as_string())

    