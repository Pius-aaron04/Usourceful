#!/usr/bin/python3
"""
Defines Recommendation table class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from os import getenv


class Recommendation(BaseModel, Base):
    """ Defines recommendation table"""

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "recommendations"
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        resource_id = Column(String(60), ForeignKey('resources.id'),
                             nullable=False)
        note = Column(String(1024), nullable=True)

    else:
        user_id = ""
        resource_id = ""
        note = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes class object
        """

        super().__init__(*args, **kwargs)
