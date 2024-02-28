#!/usr/bin/python3
"""
Defines review table
"""
from models.base_model import BaseModel, Column, String
from os import getenv


class Review(BaseModel):
    """
    Defines Review table/class
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = 'reviews'
        user_id = Column(String(60), nullable=False)
        resource_id = Column(String(60), nullable=False)
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