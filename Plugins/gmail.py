import pickle
import os
import base64
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from speak import speak
from recognize import listen_audio

# Get the path to the pickle file
home_dir = os.path.expanduser('~')
pickle_path = os.path.join(home_dir, 'gmail.pickle')

# Load our pickled credentials
creds = pickle.load(open(pickle_path, 'rb'))
sender_id = os.getenv('EMAIL_ID')

# Build the service
service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

# Create a message
def send_email(receiver_id, subject, message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_id
    msg['To'] = receiver_id
    msgPlain = message
    msg.attach(MIMEText(msgPlain, 'plain'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    message1 = body
    try:
        message2 = (
            service.users().messages().send(
                userId="me", body=message1).execute())
        return message2['labelIds'][0]
    except:
        return "ERROR OCCURRED"
