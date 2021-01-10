import email
import smtplib, ssl
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import snapshot

import email_handler

print('taking picture')
snapshot.take_picture('webcam', 'images/image.jpg')
snapshot.stop()

email_handler.send_email('images/image.jpg')