"""
Defines resource Class.
"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Resource(BaseModel, Base):
    """ Resource class for resource table"""

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = "resources"
        title = Column(String(128), nullable=False)
        rack_id = Column(String(60), ForeignKey('racks.id'))
        subrack_id = Column(String(60), ForeignKey('subracks.id'))
        description = Column(String(1024), nullable=False)
        public = Column(Boolean, default=True)
        content_type = Column(String(128), nullable=False)
        content = Column(String(4096), nullable=False)
        reviews = relationship("Review", backref="reviews")


    else:
        title = ""
        description = ""
        rack_id = ""
        public = False

        def __init__(self, *args, **kwargs):
            """ Instantiate Object """
            super().__init__(*args, **kwargs)
