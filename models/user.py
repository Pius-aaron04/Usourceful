#!/usr/bin/python3
""" Defines User class which represent the user table in the SQL database """

from models.base_model import BaseModel
import models
from os import getenv

class User(BaseModel):
    """Defines User model."""

    if getenv('USOURCE_STORAGE') == 'db':
        firstname = Column(String(128), nullable=False)
        lastname = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)

    else:
        firstname = ""
        lastname = ""
        password = ""
        email = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
