#!/usr/bin/python3
from models.base_model import BaseModel
import sqlachemy
from sqlachemy import Column, String
from sqlachemy.orm import relationship
from os import getenv


class Library(BaseModel):
    """
    Defines Library Object
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "users"
        name = Column(String(128), nullable=False)
        user_id = Column(String(60), nullable=False)
        racks = relationship("Rack", backref="user")
        reviews = relationship("Review", backref="user")
        recommendations = relationship("Recommendaion", backref="user")
    else:
        name = ""
        user_id = ""
        recommendations = []
        reviews =  []

    def __init__(self):
        """Instantiates Library Table."""

        super.__init__(*args, **kwargs)

#    if getnenv('USOURCE_STORAGE') != 'db':
