import os
import time
import smtplib
from email import encoders
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailSender:
    def __init__(self):
        self.subject = "Senior Python, Django, Flask, FastApi and Web Scrapper developer."
        self.smtp_port = os.getenv('SMTP_PORT')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
        self.sender_email_password = os.getenv('SENDER_EMAIL_PASSWORD')

    def create_email_body(self):
        email_body = """
        <html>
        <body>
            <p>I hope you're doing well. I'm impressed by your company's growth and innovation.</p>
            <p>Currently, I am working at Enzipe, one of the leading product-based companies in Pakistan. 
            With expertise in Python, Django, Flask, FastAPI, web scraping (Requests, Scrapy, Playwright, Selenium), 
            PostgreSQL, SQLite, Git, Docker, Render Server, and Heroku, I'm eager to contribute my skills.</p>
            
            <p>I'd love to discuss how I can add value to your team. My resume is attached for your review. 
            Looking forward to your response.</p>

            <p>Best regards,</p>
            <p><strong>Arslan Ahmad</strong></p>
        </body>
        </html>
        """
        return email_body

    def create_email_message(self, receiver_email):
        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['From'] = self.sender_email
        message['To'] = receiver_email

        email_body = self.create_email_body()
        message.attach(MIMEText(email_body, 'html'))

        with open("Arslan-Ahmad-Resume.pdf", "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename('Arslan-Ahmad-Resume.pdf')}")
            message.attach(part)

        return message

    def setup_smtp_server(self):
        try:
            server_credentials = smtplib.SMTP(self.smtp_server, int(self.smtp_port))
            server_credentials.starttls()
            server_credentials.login(self.sender_email, self.sender_email_password)
            return server_credentials
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate with the SMTP server. Please check your credentials.")
        except smtplib.SMTPConnectError:
            print("Failed to connect to the SMTP server. Please check the server settings.")
        except Exception as e:
            print(f"An error occurred while setting up the SMTP server: {e}")
        return None

    def send_email(self, receiver_email):
        try:
            message = self.create_email_message(receiver_email)
            server = self.setup_smtp_server()
            if server:
                server.sendmail(self.sender_email, receiver_email, message.as_string())
                server.quit()
                print(f"Email sent successfully to {receiver_email}")
            else:
                print(f"Failed to send email to {receiver_email} due to SMTP server issues.")
        except smtplib.SMTPException as e:
            print(f"An error occurred while sending the email: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def send_emails_from_file(self, email_file):
        with open(email_file, 'r') as f:
            emails = f.readlines()
        
        for email in emails:
            email = email.strip()
            if email:
                self.send_email(email)
                time.sleep(120)

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.send_emails_from_file("emails.txt")
