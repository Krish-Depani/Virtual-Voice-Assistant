import smtplib
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='..\\Data\\.env')

sender_id = os.getenv('EMAIL_ID')
password = os.getenv('PASSWORD')

def send_email(reciever_id, subject, body):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(sender_id, password)
    # message to be sent
    message = "\r\n".join([
        f"From: {sender_id}",
        f"To: {reciever_id}",
        f"Subject: {subject}",
        "",
        f"{body}"
    ])
    # sending the mail
    s.sendmail(sender_id, reciever_id, message)
    # terminating the session
    s.quit()
    return True

