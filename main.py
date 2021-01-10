import email
import smtplib, ssl
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import snapshot

import email_handler
"""
config_file = open('./config.json')
config = json.load(config_file)

message = MIMEMultipart("alternative")
message["Subject"] = "Email from Python"
message["From"] = config['sender']['username']
message["To"] = config['recipient']['username']

html = open('message.html', 'r').read()

html_obj = MIMEText(html, "html")

message.attach(html_obj)
"""

print('taking picture')
snapshot.take_picture('webcam', 'images/image.jpg')
snapshot.stop()
print('done')

print('about to send email')
email_handler.send_email('images/image.jpg')
print('all done')

"""
filename = 'images/image.jpg'

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

context = ssl.create_default_context() # Create a secure SSL context
with smtplib.SMTP_SSL(
    config['sender']['server'], config['sender']['port'], context=context
) as server:
    try:
        server.login(config['sender']['username'], config['sender']['password'])
        try:
            server.sendmail(
                config['sender']['username'], config['recipient']['username'], message.as_string())
            print("Sent the email")
        except smtplib.SMTPException as err:
            print('An error occurred while sending the email: \n', err)
    except smtplib.SMTPException as err:
        print("Could not log into the email server. Please check \
            that the 'sender' values are correct in config.json.")
        print('Error:\n', err)
    finally:
        server.quit()
        """