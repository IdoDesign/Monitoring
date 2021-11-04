from checks import *

class Host:
    def __init__(self, hostname, description) -> None:
        self.hostname = hostname
        self.descriptions = description
        self.checks = []
    
    def add_check(self, name, description, check_type, wait_time, port=None):
        if check_type == 'tcp':
            self.checks.append(TCP_Check(name, description, wait_time, self.hostname, port))
        elif check_type == 'icmp':
            self.checks.append(ICMP_Check(name, description, wait_time, self.hostname))
    
    def every_check_one_time(self):
        for check in self.checks:
            print(check.single_check()) 