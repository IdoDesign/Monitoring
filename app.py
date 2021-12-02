import json, jsonschema
import threading
import logging
import utils
from configparser import ConfigParser
from base import engine, Base

def main(filepath):
    FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
    DATE_FORMAT = "%d-%b-%y %H:%M:%S"
    
    #Set logging formats
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT)
    file_handler = logging.FileHandler('results.log')
    file_handler.setFormatter(logging.Formatter(FORMAT, DATE_FORMAT))
    logging.getLogger().addHandler(file_handler)
    
    # creating a thread for each host
    hosts = utils.load_data(filepath)
    if hosts:
        for host in hosts:
            logging.info("Started monitoring script")
            threading.Thread(target=host.check_thereaded).start()

Base.metadata.create_all(engine)

if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')

    main(config['DATA']['FILEPATH'])