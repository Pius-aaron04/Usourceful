#!/usr/bin/python3
""" Defines database storage model."""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.library import Library
from models.resource import Resource
from models.review import Review
from models.rack import Rack
from models.sub_rack import Subrack
from models.recommendation import Recommendation


class DBStorage:
    """Database Storage System"""

    __engine = None
    __session = None
    classes = {
                'User': User,
                'Library': Library,
                'Rack': Rack,
                'Subrack': Subrack,
                'Resource': Resource,
                'Review': Review,
                'Recommendation': Recommendation
              }

    def __init__(self):
        """ instantiate storage object """

        USER = getenv('USOURCE_USER')
        HOST = getenv('USOURCE_HOST')
        PWD = getenv('USOURCE_PWD')
        DB = getenv('USOURCE_DB')
        ENV = getenv('USOURCE_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB))

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """
        Adds an obj to the database
        """
        self.__session.add(obj)

    def all(self, cls=None):
        """ returns all cls instance """

        all_objects = {}

        for clss in self.classes:
            if cls or clss is self.classes[clss] or cls is None:
                objs = self.__session.query(self.classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    all_objects[key] = obj
        return (all_objects)

    def reload(self):
        """
        loads data from database.
        """

        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """
        Closes session
        """

        self.__session.remove()

    def save(self):
        """
        Commits changes
        """

        self.__session.commit()

    def delete(self, obj=None):
        """
        removes an object from database.
        """

        if obj and obj in self.all(obj.__class__).values():
            self.__session.delete(obj)
