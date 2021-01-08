import smtplib, ssl
import json
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
html = """\
<html>
  <body>
    <p>Hello from a Python Script!<br>
       This is a second line<br>
       <a href="http://www.google.com">Hyperlink</a>
       some plain text
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

context = ssl.create_default_context() # Create a secure SSL context

with smtplib.SMTP_SSL(
    config['sender']['server'], config['sender']['port'], context=context
) as server:
    server.login(config['sender']['username'], config['sender']['password'])
    
    server.sendmail(
        config['sender']['username'], config['recipient']['username'], message.as_string())

    print('Attempted to send email')