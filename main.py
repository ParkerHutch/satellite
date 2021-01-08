import smtplib, ssl
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config_file = open('./config.json')
config = json.load(config_file)

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = config['sender']['username']
message["To"] = config['recipient']['username']

# Create the plain-text and HTML version of your message
text = """\
Python script message
"""
html = open('message.html', 'r').read()

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

context = ssl.create_default_context() # Create a secure SSL context


filename = "attachment.jpg"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

message.attach(part) # attach attachment

with smtplib.SMTP_SSL(
    config['sender']['server'], config['sender']['port'], context=context
) as server:
    server.login(config['sender']['username'], config['sender']['password'])
    server.sendmail(
        config['sender']['username'], config['recipient']['username'], message.as_string())
    print('Attempted to send email')