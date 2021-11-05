import json
import threading
import logging
from configparser import ConfigParser
from host import Host


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

    # creating a host object for each one in json file
    for host in data['hosts']:
        hosts.append(Host(host))

    return hosts

def main(filepath):
    FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
    DATE_FORMAT = "%d-%b-%y %H:%M:%S"
    
    #Set logging formats
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT)
    file_handler = logging.FileHandler('results.log')
    file_handler.setFormatter(logging.Formatter(FORMAT, DATE_FORMAT))
    logging.getLogger().addHandler(file_handler)
    
    # creating a thread for each host
    for host in load_data(filepath):
        logging.info("Started monitoring script")
        threading.Thread(target=host.check_thereaded).start()


if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')

    main(config['DATA']['FILEPATH'])