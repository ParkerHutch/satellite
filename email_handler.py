import json
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path, walk

config_file = open('./config.json')
config = json.load(config_file)

def get_attachment_paths(attachments_path):
    paths = []
    _, _, filenames = next(walk(attachments_path))
    for filename in filenames:
        paths.append(path.join(attachments_path, filename))
    return paths

def attach_file(message, attachment_path):
    # Open the attachment in binary reading mode
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part) # Encode file in ASCII characters to send by email

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    message.attach(part) # attach attachment

def send_email(attachments_path): # TODO make attachments an array
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

    for attachment_path in get_attachment_paths(attachments_path):
        attach_file(message, attachment_path)
    
    """ 
        Send the email
    """
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
