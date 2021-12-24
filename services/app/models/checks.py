import logging
import time
import utils
import uuid

from contextlib import contextmanager
from sqlalchemy import Column, String, Boolean, Integer, update

from base import Base, Session
from models.heartbeat import Heartbeat

class Check(Base):
    """Check is a simple class that represent one check for one host

    Attributes:
        name (str): The name of the check
        description (str): Describes the check and it's purpose
        hostname (str): The hostname the check is refrering
        wait_time (int): Time in seconds between Checks
        max_attempts (int): Number of maximum attempts before changing status

    """

    __tablename__ = 'checks'
    _id = Column(String(250), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    wait_time = Column(Integer, nullable=False)
    max_attempts = Column(Integer, nullable=False)
    is_up = Column(Boolean, nullable=False)
    type = Column(String(10), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'checks',
        'polymorphic_on': type
    }

    def __init__(self, name: str, description: str, hostname: str, wait_time: int, max_attempts: int, _id=None):
        """Creates a simple check Host"""
        self._id = uuid.uuid4().hex if _id is None else _id
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
        session = Session()
        stmt = update(Check).where(Check._id == self._id).values(is_up=self.is_up).execution_options(synchronize_session=False)
        result = session.execute(stmt)
        session.commit()
        session.close()

    def check(self):
        """Checks if the hostname is avaylable

        Every wait time period, does the check, 
        if check failed number of times, will send email, and change check status.
        Then, if the check is successfull, changes the staus back and sends an email.

        """
        self.count = 0
        logging.info(f"Started monitoring {self.name}")

        while True:
            if self.is_up:
                if self.heartbeat():
                    self.count = 0
                else:
                    self.count += 1
                    if self.count > self.max_attempts:
                        logging.error("{} status changed to down, please check {}".format(
                            self.name, self.hostname))
                        utils.send_alert("{} is down".format(
                            self.name), "{} failed 5 times, please check {}".format(self.name, self.hostname), False)
                        self.change_status()
                time.sleep(self.wait_time)

            if not self.is_up:
                if self.heartbeat():
                    self.count += 1
                    if self.count > self.max_attempts:
                        logging.error("{} status changed to up".format(self.name))
                        utils.send_alert("{} is up".format(self.name), "{} succeeded 5 times".format(self.name, self.hostname), True)
                        self.change_status()
                else:
                    self.count = 0

                time.sleep(self.wait_time)
    
    def heartbeat(self) -> bool:
        """Calls for a heartbeat check and saves result to DB"""
        start_time = time.time()
        result = self.single_check()
        end_time = time.time()
        response_time = end_time - start_time if result else 0
        hb = Heartbeat(self.name, self.hostname, result, response_time)
        session = Session()
        session.add(hb)
        session.commit()
        session.close()

        return result


class TCP_Check(Check):
    """A TCP Check

    Attributes:
        type (str): Indicate that check is of type 'tcp'
        port (int): The tcp port number

    """

    port = Column(Integer)
    __mapper_args__ = {'polymorphic_identity': 'tcp'}

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
    __mapper_args__ = {'polymorphic_identity': 'icmp'}

    def __init__(self, name: str, description: str, hostname: str,  wait_time: int, max_attempts: int):
        super().__init__(name, description, hostname, wait_time, max_attempts)
        self.type = 'icmp'

    def single_check(self) -> bool:
        return utils.ping(self.hostname)
