"""
Defines resource Class.
"""
from models.base_model import BaseModel
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class Resource(BaseModel):
    """ Resource class for resource table"""

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "resources"
        title = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        rack_id = Column(String(60), nullable=False)
        public = Column(Boolean, default=False)
        reviews = relationship("Review", backref="Resource")

    else:
        title = ""
        description = ""
        rack_id = ""
        public = False

        def __init__(self, *args, **kwargs):
            """ Instantiate Object """
            super().__init__(*args, **kwargs)
