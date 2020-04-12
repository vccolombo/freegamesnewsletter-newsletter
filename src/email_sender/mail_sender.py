import smtplib, ssl

class MailSender:
    sender_email = "freegamesnewsletter@gmail.com"
    sender_password = ""

    # smtp configs
    smtp_domain = "smtp.gmail.com"
    smtp_port = 465

    def send(self, contact_list):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_domain, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)

            for contact in contact_list:
                self._send_mail(contact, server)

    def _send_mail(self, contact, server):
        receiver_email = contact.email

        message = "Hello World"

        server.sendmail(self.sender_email, receiver_email, message)