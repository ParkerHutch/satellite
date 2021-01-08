import smtplib, ssl
import json

config_file = open('./config.json')
config = json.load(config_file)

message = """\
Subject: Hi there

This message was sent from a Python script."""

port = 465 # SSL
context = ssl.create_default_context() # Create a secure SSL context

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(config['sender']['username'], config['sender']['password'])
    server.sendmail(
        config['sender']['username'], config['recipient']['username'], message)
    print('Attempted to send email')