import socket
import os
import smtplib
import ssl

from configparser import ConfigParser


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


def send_mail(subject: str, message: str):
    """Sends plain text e-mail 

    Args:
        subject (str): Subject of Email
        message (str): The message of email
    """
    config = ConfigParser()
    config.read('config.ini')
    mail_config = config['MAIL']

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail_config['SENDER'],
                     mail_config['PASSWORD'])
        server.sendmail(mail_config['SENDER'], mail_config['RECEIVER'],
                        f"Subject: {subject} \n{message}\n\n Monitor.ido")
