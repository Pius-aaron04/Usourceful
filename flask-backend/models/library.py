#!/usr/bin/python3
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from decouple import config
import os
from shutil import rmtree

BASEDIR = os.path.join(os.path.expanduser('~'), 'usource')


class Library(BaseModel, Base):
    """
    Defines Library Object
    """

    if config('USOURCE_STORAGE') == 'db':
        __tablename__ = "libraries"
        name = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        racks = relationship("Rack", backref="library", cascade="all, delete-orphan")
    else:
        name = ""
        user_id = ""
        reviews = []

    def __init__(self, *args, **kwargs):
        """Instantiates Library Table."""

        super().__init__(*args, **kwargs)

        user_dir = os.path.join(BASEDIR, self.id)

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            sub_dirs = ['images', 'videos', 'pdfs']

            for path in sub_dirs:
                os.makedirs(os.path.join(user_dir, path))

    @property
    def num_racks(self):
        """
        calculates number of racks in the library
        """

        return len(self.racks) if self.racks else 0

    def delete(self):
        """
        deletes instance from storage.
        """
        from models import storage

        user_dir = os.path.join(BASEDIR, self.id)

        if os.path.exists(user_dir):
            rmtree(user_dir)
        storage.delete(self)
        storage.save()
