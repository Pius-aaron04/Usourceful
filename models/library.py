#!/usr/bin/python3
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class Library(BaseModel, Base):
    """
    Defines Library Object
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "libraries"
        name = Column(String(128), nullable=False)
        user_id = Column(String(60), nullable=False)
        racks = relationship("Rack", backref="libraries")
        reviews = relationship("Review", backref="libraries")
    else:
        name = ""
        user_id = ""
        recommendations = []
        reviews =  []

    def __init__(self, *args, **kwargs):
        """Instantiates Library Table."""

        super.__init__(*args, **kwargs)

#    if getnenv('USOURCE_STORAGE') != 'db':
