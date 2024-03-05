#!/usr/bin/python3
"""
Defines review table
"""
from models.base_model import BaseModel, Column, String, Base
from os import getenv
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """
    Defines Review table/class
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = 'reviews'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        resource_id = Column(String(60), ForeignKey('resources.id'),
                             nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        user_id = ""
        resource_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes class object
        """
        super().__init__(*args, **kwargs)
