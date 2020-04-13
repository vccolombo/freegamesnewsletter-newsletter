import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from game import Game

class MailSender:
    sender_email = "freegamesnewsletter@gmail.com"
    sender_password = os.environ["FREEGAMESNEWSLETTER_PASSWORD"]

    # smtp configs
    smtp_domain = "smtp.gmail.com"
    smtp_port = 465

    def send(self, contact_list):
        games_list = Game.get_todays_free_games()
        smtp_client = self._create_smtp_connection()

        for contact in contact_list:
            games_for_this_contact = self._get_games_for_contact(contact, games_list)
            if games_for_this_contact:
                message = self._generate_message(contact, games_for_this_contact)
                self._send_mail(contact, message, smtp_client)
            
        smtp_client.quit()

    def _create_smtp_connection(self):
        context = ssl.create_default_context()
        smtp_client = smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, context=context)
        smtp_client.login(self.sender_email, self.sender_password)
        return smtp_client

    def _send_mail(self, receiver, message, smtp_client):
        receiver_email = receiver.email
        smtp_client.sendmail(self.sender_email, receiver_email, message.as_string())

    def _get_games_for_contact(self, contact, games_list):
        return games_list

    def _generate_message(self, receiver, games_list):
        message = MIMEMultipart("alternative")
        message["Subject"] = "These games are free-to-keep today"
        message["From"] = self.sender_email
        message["To"] = receiver.email

        text_msg = self._generate_text_message(games_list)
        html_msg = self._generate_html_message(games_list)

        message.attach(MIMEText(text_msg, "plain"))
        message.attach(MIMEText(html_msg, "html"))

        return message
    
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