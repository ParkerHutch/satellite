import smtplib, ssl
import json

f = open('./userinfo.json')
data = json.load(f)
print(data['username'])

"""
port = 465 # SSL
password = input("Type password:")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("my@gmail.com", password)
    # TODO: Send email here

print("Hello, World!")"""