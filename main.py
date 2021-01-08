import smtplib, ssl
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config_file = open('./config.json')
config = json.load(config_file)

message = MIMEMultipart("alternative")
message["Subject"] = "Email from Python"
message["From"] = config['sender']['username']
message["To"] = config['recipient']['username']

"""
    Create the HTML part of the message
"""
html = open('message.html', 'r').read()

html_obj = MIMEText(html, "html")

message.attach(html_obj)

"""
    Create the attachment part of the message
"""
filename = "attachment.jpg"  # In same directory as script

# Open the attachment in binary reading mode
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part) # Encode file in ASCII characters to send by email

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

message.attach(part) # attach attachment

""" 
    Send the email
"""
context = ssl.create_default_context() # Create a secure SSL context
with smtplib.SMTP_SSL(
    config['sender']['server'], config['sender']['port'], context=context
) as server:
    server.login(config['sender']['username'], config['sender']['password'])
    server.sendmail(
        config['sender']['username'], config['recipient']['username'], message.as_string())
    print('Attempted to send email')