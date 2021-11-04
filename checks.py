import time
import utils

class Check:
    def __init__(self, name, description, hostname, wait_time):
        self.name = name
        self.description = description
        self.hostname = hostname
        self.wait_time = wait_time

    def check(self):
        self.single_check()

class TCP_Check(Check):
    def __init__(self, name, description, hostname, wait_time, port):
        super().__init__(name, description, wait_time, hostname)
        self.type = 'tcp'
        self.port = port

    def single_check(self):
        utils.tcp_ping(self.hostname, self.port)

class ICMP_Check(Check):
    def __init__(self, name, description,hostname,  wait_time):
        super().__init__(name, description, hostname, wait_time)
        self.type = 'icmp'

    def single_check(self):
        utils.ping(self.hostname)
    