import smtplib, ssl
import json

config_file = open('./config.json')
config = json.load(config_file)

message = """\
Subject: Hi there

This message was sent from a Python script."""

context = ssl.create_default_context() # Create a secure SSL context

with smtplib.SMTP_SSL(
    config['sender']['server'], config['sender']['port'], context=context
) as server:
    server.login(config['sender']['username'], config['sender']['password'])
    server.sendmail(
        config['sender']['username'], config['recipient']['username'], message)
    print('Attempted to send email')