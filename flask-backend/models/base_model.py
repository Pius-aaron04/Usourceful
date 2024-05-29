#!/usr/bin/python3
"""
This is the foundation of every data model in the database.
"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from decouple import config

if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object
time = '%Y-%m-%dT%H:%M:%S.%f'


class BaseModel:
    """
    The Super class for all data models from which future data classes will be
    derived.
    """

    if config('USOURCE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True, default=str(uuid4()))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)
    else:
        id = str(uuid4())
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        """ Instantiates a new model."""
        if kwargs:
            # sets instance attributes from keyword arguments
            if '__class__' in kwargs:
                del kwargs['__class__']
            for k, v in kwargs.items():
                if k in ('updated_at', 'created_at'):
                    setattr(self, k, datetime.fromisoformat(v))
                else:
                    setattr(self, k, v)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid4()))

        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """ String representation of thr instance."""

        cls = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """saves the changes in the instance attributes"""

        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """returns a dictionary of attributes."""

        attributes = self.__dict__.copy()
        attributes['__class__'] = self.__class__.__name__

        if self.__class__.__name__ in ("Rack", "Library"):
            attributes['num_items'] = self.num_items

        if 'created_at' in attributes:
            attributes['created_at'] = attributes['created_at'].strftime(time)
        if 'updated_at' in attributes:
            attributes['updated_at'] = attributes['updated_at'].strftime(time)
        if '_sa_instance_state' in attributes:
            del attributes['_sa_instance_state']
        del attributes['__class__']
        return attributes

    def update(self, **kwargs):
        """ update instance attributes."""

        if kwargs:
            for k, v in kwargs.items():
                if k not in ('id', 'updated_at', 'created_at'):
                    setattr(self, k, v)
        self.save()
        return self.to_dict()

    def delete(self):
        """
        deletes instance from storage.
        """
        from models import storage

        storage.delete(self)
        storage.save()
