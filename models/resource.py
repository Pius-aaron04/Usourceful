"""
Defines resource Class.
"""
from models.base_model import BaseModel
from os import getenv
import sqlachemy
from sqlachemy import Column, String, Boolean


class Resource(BaseModel):
    """ Resource class for resource table"""

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "resources"
        title = Column(String(128), nullable=False)
        description = column(String(1024), nullable=False)
        rack_id = Column(String(60), nullable=False)
        public = Column(Boolean, default=False)

    else:
        title = ""
        description = ""
        rack_id = ""
        public = False

        def __init__(self, *args, **kwargs):
            """ Instantiate Object """
            super().__init__(*args, **kwargs)
