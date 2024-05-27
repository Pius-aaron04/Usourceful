#!/usr/bin/python3
""" Defines database storage model."""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from decouple import config
from models.base_model import Base
from models.user import User
from models.library import Library
from models.resource import Resource, Video, Text, Image
from models.review import Review, RackReview, ResourceReview
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
                'Recommendation': Recommendation,
                'RackReview': RackReview,
                'ResourceReview': ResourceReview,
                'Video': Video,
                'Image': Image,
                'Text': Text
              }

    def __init__(self):
        """ instantiate storage object """

        USER = config('USOURCE_USER')
        HOST = config('USOURCE_HOST')
        PWD = config('USOURCE_PWD')
        DB = config('USOURCE_DB')
        ENV = config('USOURCE_ENV')
        dialete = config('DIALETE')
        if 'sqlite' not in dialete:
            self.__engine = create_engine('{}://{}:{}@{}/{}'.
                                          format(dialete, USER, PWD, HOST,
                                                 DB))
        self.__engine = create_engine('sqlite:///database.db')

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
            if cls is None or cls is self.classes[clss] or cls is clss:
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

    def find(self, _cls, credent):
        """ Returns a class object"""

        return self.__session.query(_cls).filter_by(username=credent)

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

    def get(self, cls, _id):
        """
        retrieves an object
        """

        key = cls.__name__ + '.' + _id
        data = self.all(cls)
        if key not in data:
            return None

        return data[key]

    def delete(self, obj=None):
        """
        removes an object from database.
        """

        if obj and obj in self.all(obj.__class__).values():
            self.__session.delete(obj)

    def rollback(self):
        """
        rollback database if faiure occurs during flush
        """

        self.__session.rollback()
