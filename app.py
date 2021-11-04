import json, threading
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

    #creating a host object for each one in json file
    for host in data['hosts']:
        hosts.append(Host(host))
    
    return hosts

def main(filepath):
    for host in load_data(filepath):
        #creating a thread for each host
        threading.Thread(target= host.check_thereaded).start()

if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')
    
    main(config['DATA']['FILEPATH'])