import threading, logging
from checks import *


class Host:
    """Host class that represent one host with one IP address

    Each host represents one server or computer.
    You can add multiple checks for each host.

    Attributes:
        hostname: A string of hostname or IP address
        description: A string thed describe the host server or computer
    """

    def __init__(self, hostname: str, description: str):
        """Creats a simple host objects"""

        self.hostname = hostname
        self.descriptions = description
        self.checks = []

    def __init__(self, host: dict):
        """Creates a host object from dict"""

        self.hostname = host['hostname']
        self.descriptions = host['description']
        self.checks = []
        
        for check in host['checks']:

            if check["type"] == 'tcp':
                self.checks.append(TCP_Check(
                    check["name"], check["description"], self.hostname, check["wait_time"], check['max_attempts'], check["port"]))

            elif check["type"] == 'icmp':
                self.checks.append(ICMP_Check(
                    check["name"], check["description"], self.hostname, check["wait_time"], check['max_attempts']))

    def add_check(self, name: str, description: str, check_type: str, wait_time: int, max_attempts: int, port: int = None):
        """Adds a check to the check list of the host

        Args:
            name (str): The check's name
            description (str): The check's description' or purpose
            check_type (str): tcp or udp
            wait_time (int): Time between checks, in seconds
            max_attempts (int): Number of max_attempts before changing status
            port (int, optional): Port number for tcp checks. Defaults to None.
        """

        if check_type == 'tcp':
            self.checks.append(TCP_Check(name, description,
                               self.hostname, wait_time, port))
        elif check_type == 'icmp':
            self.checks.append(ICMP_Check(
                name, description, self.hostname, wait_time))

    def every_check_one_time(self):
        for check in self.checks:
            check.single_check()

    def check_thereaded(self):
        logging.info(f"Started monitoring {self.hostname}")
        for check in self.checks:
            threading.Thread(target=check.check).start()
