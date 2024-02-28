#!/usr/bin/python3
""" Defines database storage model."""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base

class DBStorage:
    """Database Storage System"""

    __engine = None
    __session = None

    def __init__(self):
        """ instantiate storage object """

        USER = getenv('USOURCE_STORAGE')
        HOST = getenv('USOURCE_HOST')
        PWD = getenv('USOURCE_PWD')
        DB = getenv('USOURCE_DB')
        ENV = getenv('USOURCE_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB))

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns all cls instance """


