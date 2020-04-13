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
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)

            for contact in contact_list:
                message = self._generate_message(contact)
                self._send_mail(contact, message, server)
            
            server.quit()

    def _send_mail(self, receiver, message, server):
        receiver_email = receiver.email
        server.sendmail(self.sender_email, receiver_email, message.as_string())

    def _generate_message(self, receiver):
        message = MIMEMultipart("alternative")
        message["Subject"] = "These games are free-to-keep today"
        message["From"] = self.sender_email
        message["To"] = receiver.email

        games_list = Game.get_games()
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