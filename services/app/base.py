import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#load enviorment vars
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('SQL_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
SQL_PORT = os.getenv('SQL_PORT')

engine = create_engine(
    'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, SQL_PORT, POSTGRES_DB))
Session = sessionmaker(bind=engine)

Base = declarative_base()
