import json
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path, walk
from typing import List

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

def get_file_paths(folder_path: str) -> List[str]:
    """Get the paths to all files in the folder given by the path 
    folder_path.

    Args:
        folder_path (str): the path to the folder containing files

    Returns:
        List[str]: a list of filepaths as strings corresponding to files in the 
        given folder
    """

    paths = []
    _, _, filenames = next(walk(folder_path))
    for filename in filenames:
        paths.append(path.join(folder_path, filename))
    return paths

def attach_file(message: MIMEMultipart, attachment_path: str):
    """Attach the attachment with given file path to the given email message.

    Args:
        message (MIMEMultipart): the email message to add an attachment to
        attachment_path (str): the path to the attachment file
    """

    # Open the attachment in binary reading mode
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    message.attach(part) # attach attachment

def send_email(attachments_folder_path, verbose:bool = False):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email from Python"
    message["From"] = config['sender']['username']
    message["To"] = config['recipient']['username']

    """
        Create the HTML part of the message
    """
    html = open('email-message.html', 'r').read()

    html_obj = MIMEText(html, "html")

    message.attach(html_obj)

    for attachment_path in get_file_paths(attachments_folder_path):
        attach_file(message, attachment_path)
    
    """ 
        Send the email
    """
    context = ssl.create_default_context() # Create a secure SSL context
    with smtplib.SMTP_SSL(
        config['sender']['server'], config['sender']['port'], context=context
    ) as server:
        try:
            server.login(config['sender']['username'], 
                            config['sender']['password'])
            if verbose:
                print('Logged into the email server')
            try:
                server.sendmail(config['sender']['username'], 
                                config['recipient']['username'], 
                                message.as_string())
                if verbose:
                    print("Sent the email")
            except smtplib.SMTPException as err:
                print('An error occurred while sending the email: \n', err)
        except smtplib.SMTPException as err:
            print("Could not log into the email server. Please check \
                that the 'sender' values are correct in config.json.")
            print('Error:\n', err)
        finally:
            server.quit()
