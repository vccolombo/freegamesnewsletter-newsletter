import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import calendar
import os
import logging


from game import Game

class MailSender:
    sender_email = "freegamesnewsletter@gmail.com"
    sender_password = os.environ["FREEGAMESNEWSLETTER_PASSWORD"]

    # smtp configs
    smtp_domain = "smtp.gmail.com"
    smtp_port = 465

    def send(self, contact_list):
        smtp_client = self._create_smtp_connection()
        
        games_to_send = self._get_games_to_send()
        if games_to_send:
            logging.info(f"Sending {len(games_to_send)} games...")
            message = self._generate_message(games_to_send)
            for receiver in contact_list:
                message["To"] = receiver.email
                self._send_mail(receiver, message, smtp_client)
        else:
            logging.info("No games to send today")
            
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

    def _generate_message(self, games_list):
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["Subject"] = self._generate_subject()
        message["X-Priority"] = "3"

        text_msg = self._generate_text_message(games_list)
        html_msg = self._generate_html_message(games_list)

        message.attach(MIMEText(text_msg, "plain"))
        message.attach(MIMEText(html_msg, "html"))

        return message
    
    def _generate_subject(self):
        today = datetime.now()
        day = str(today.day)
        month = calendar.month_abbr[today.month]

        return f"Free-to-keep games {day} {month}"

    def _generate_text_message(self, games_list):
        msg = "Hello!\nThese games are free to grab and keep forever:\n\n"
        for game in games_list:
            msg += f"{game.name}: {game.url}\n"
        
        return msg

    def _generate_html_message(self, games_list):
        msg = ""
        for game in games_list:
            msg += f"<div><a href='{game.url}'>{game.name}</a></div>"

        html = f"""\
            <body>
                <p> Hello!<br>
                    These games are free to grab and keep forever:
                </p>
                <div>
                    {msg}
                </div>
            </body>
        """
        return html

    def _send_mail(self, receiver, message, smtp_client):
        receiver_email = receiver.email
        smtp_client.sendmail(self.sender_email, receiver_email, message.as_string())

    