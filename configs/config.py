import configparser
import os

dirname, filename = os.path.split(os.path.abspath(__file__))
config_path = os.path.join(dirname, 'config.ini')
config = configparser.ConfigParser()


config.read(config_path)
TOKEN = config['API']['TOKEN']
CHAT_ID = config['API']['CHAT_ID']

