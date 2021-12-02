from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = ConfigParser()
config.read('config.ini')
db_config = config['POSTGRES']

engine = create_engine(
    'postgresql+psycopg2://{}:{}@{}:5432/{}'.format(db_config['POSTGRES_USER'], db_config['POSTGRES_PASSWORD'], db_config['POSTGRES_HOST'], db_config['POSTGRES_DB']))
Session = sessionmaker(bind=engine)

Base = declarative_base()
