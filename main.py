import smtplib, ssl
import json

account_info_file = open('./accountinfo.json')
account_info = json.load(account_info_file)


port = 465 # SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(account_info['username'], account_info['password'])
    # TODO: Send email here

print("Hello, World!")