#!/usr/bin/python3
""" Defines User class which represent the user table in the SQL database """

from models.base_model import BaseModel, Column, String, Base
import models
from os import getenv
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Defines User model."""

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = 'users'
        firstname = Column(String(128), nullable=False)
        lastname = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        recommendations =  relationship("Recommendations", backref="users")
        #library = relationship("Library", backref="users")

    else:
        firstname = ""
        lastname = ""
        password = ""
        email = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
