import socket
import os
import smtplib
import ssl
import logging
import json, jsonschema
from configparser import ConfigParser
import requests
import base64
from models.host import Host

config = ConfigParser()
config.read('config.ini')

def ping(hostname: str) -> bool:
    """Send ICMP packet to server

    using the PING command, sends a ICMP request to the server,
    if there is a reply, returns true.

    Args:
        hostname (str): The hostname or ip of the server

    Returns:
        bool: Returns true if the ping was succsessfull
    """

    # cli ping will not show up because of '> /dev/null 2>&1'
    command = "ping -c 1 {} > /dev/null 2>&1".format(hostname)
    response = os.system(command)
    if response == 0:
        return True
    else:
        return False

def tcp_ping(hostname: str, port: int) -> bool:
    """openes a tcp socket to Hostname in given port"

    Args:
        hostname (str): The hostname or ip of the server
        port (int): the port number for the tcp connection

    Returns:
        bool: Returns true if the socket opening was succsessfull
    """

    try:
        sock = socket.socket()
        sock.connect((hostname, port))
        return True
    except:
        return False
    finally:
        sock.close()

def send_alert(subject: str, message: str, is_up: bool):
    """Sends alerts to the user

    Sends alerts based on user configuration file, Mail, PushSafer or both.

    Args:
        subject (str): alert subject
        message (str): alert message
    """
    if config['MAIL']['SENDER']:
        send_mail(subject, message)
    if config['PUSH_SAFER']['PUSH_API_KEY']:
        send_notification(subject, message, is_up)

def send_mail(subject: str, message: str):
    """Sends plain text e-mail 

    Args:
        subject (str): Subject of Email
        message (str): The message of email
    """
    mail_config = config['MAIL']

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            #Logging in to Gmail account
            server.login(mail_config['SENDER'], mail_config['PASSWORD'])
            #Sending email
            server.sendmail(mail_config['SENDER'], mail_config['RECEIVER'],
                    f"Subject: {subject} \n{message}\n\n Monitor.ido")

        except smtplib.SMTPAuthenticationError() as e:
            logging.error("Authentication to SMTP server failed, please check your config file")

def send_notification(subject: str, message: str, is_up: bool):
    """Sends notificaetions with PushSafer API

    Args:
        subject (str): Subject of the notification
        message (str): The message in the notification
    """
    push_config = config['PUSH_SAFER']
    image_path = "icons/green_tick.png" if is_up  else "icons/Warning.png"
    image = open(image_path, 'rb')
    image_read = image.read()
    image1 = base64.encodebytes(image_read)
    url = '{}/api'.format(push_config['PUSH_URL'])
    post_fields = {
        "t" : subject,
        "m" : message,
        "v" : 3,
        "i" : 33,
        "c" : '#FF0000',
        "d" : 'a',
        "u" : push_config['PUSH_URL'],
        "ut": 'Open Pushsafer',
        "k" : push_config['PUSH_API_KEY'],
        "p" : 'data:image/png;base64,'+str(image1.decode('ascii'))
    }
    try:  
        r = requests.post(url, data=post_fields)
        logging.info("Notification was sent succsessfully to PushSafer API, response:{}".format(r.text))
    except requests.exceptions.ConnectionError as err:
        logging.error("Failed to send notification to PushSafer")

def load_data(filepath) -> list:
    """Loading data from json file to create a hosts list

    Args:
        filepath (str): path to json data file.

    Returns:
        list: List of Hosts 
    """
    hosts = []

    file = open(filepath, 'r')
    data = json.load(file)
    file.close()
    
    if vaildate_json(data):
        # creating a host object for each one in json file
        for host in data['hosts']:
            hosts.append(Host(host))
        return hosts
    return None

def vaildate_json(jsonData: dict) -> bool:
    """validating the data json to prevent errors in run time

    Using JSON schema, checks the validity of the JSON file.
    If file is not valid, return False

    Args:
        jsonData (dict): data from JSON file as dictionary

    Returns:
        bool: Returns True if Json is valid
    """
    #Loading schema file
    schema_file = open("schema.json", 'r')
    schema = json.load(schema_file)
    schema_file.close()

    try:
        jsonschema.validate(jsonData,schema)
    except jsonschema.exceptions.ValidationError as err:
        logging.error(err)
        return False
    return True