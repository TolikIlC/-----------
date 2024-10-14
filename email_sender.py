import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

        def load_users_from_json(self, filename):
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    users = json.load(file)
                    return users
            except Exception as e:
                print(f"Ошибка при загрузке пользователей: {e}")
                return []
        
        def send_email(self, recipient, subject, body):
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                    print(f"Письмо успешно отправлено на {recipient}")
            except Exception as e:
                print(f"Ошибка при отправке письма на {recipient}")

        def send_bulk_emails(self, json_filename, subject, body):
            users = self.load_users_from_json(json_filename)

            for user in users:
                if 'email' in user:
                    self.send_email(user['email'], subject, body)