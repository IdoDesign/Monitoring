import logging
import time
import utils

class Check:
    """Check is a simple class that represent one check for one host

    Attributes:
        name (str): The name of the check
        description (str): Describes the check and it's purpose
        hostname (str): The hostname the check is refrering
        wait_time (int): Time in seconds between Checks
        max_attempts (int): Number of maximum attempts before changing status

    """
    
    def __init__(self, name: str, description: str, hostname: str, wait_time: int, max_attempts: int):
        """Creates a simple check Host"""
        self.name = name
        self.description = description
        self.hostname = hostname
        self.wait_time = wait_time
        self.max_attempts = max_attempts
        self.is_up = True
        self.count = 0

    def change_status(self):
        """Changes the status of the check"""

        self.is_up = not self.is_up
        self.count = 0
    
    def check(self):
        """Checks if the hostname is avaylable
        
        Every wait time period, does the check, 
        if check failed number of times, will send email, and change check status.
        Then, if the check is successfull, changes the staus back and sends an email.

        """
        logging.info(f"Started monitoring {self.name}")

        while True:
            if self.is_up:
                if self.single_check():
                    self.count = 0
                else:
                    self.count += 1
                    if self.count > self.max_attempts:
                        logging.error("{} status changed to down, please check {}".format(self.name, self.hostname))
                        utils.send_alert("{} is down".format(self.name),"{} failed 5 times, please check {}".format(self.name, self.hostname))
                        self.change_status()
                        
                time.sleep(self.wait_time)
            
            if not self.is_up:
                if self.single_check():
                    self.count += 1
                    if self.count > self.max_attempts:
                        logging.error("{} status changed to up".format(self.name))
                        utils.send_alert("{} is up".format(self.name),"{} succeeded 5 times".format(self.name, self.hostname))
                        self.change_status()
                else:
                    self.count = 0
                   
                time.sleep(self.wait_time)
  
class TCP_Check(Check):
    """A TCP Check

    Attributes:
        type (str): Indicate that check is of type 'tcp'
        port (int): The tcp port number

    """
    def __init__(self, name: str, description: str, hostname: str, wait_time: int, max_attempts: int, port: int):
        super().__init__(name, description, hostname, wait_time, max_attempts)
        self.type = 'tcp'
        self.port = port

    def single_check(self) -> bool:
        return utils.tcp_ping(self.hostname, self.port)

class ICMP_Check(Check):
    """An ICMP Check

    Attributes:
        type (str): Indicate that check is of type 'icmp'

    """
    def __init__(self, name: str, description: str, hostname:str,  wait_time: int, max_attempts:int):
        super().__init__(name, description, hostname, wait_time, max_attempts)
        self.type = 'icmp'

    def single_check(self) -> bool:
        return utils.ping(self.hostname)
    