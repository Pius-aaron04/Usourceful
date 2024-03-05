"""
Defines resource Class.
"""
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

storage_type = getenv('USOURCE_STORAGE')

class Resource(BaseModel, Base):
    """ Resource class for resource table"""

    if storage_type == 'db':
        __tablename__ = "resources"
        title = Column(String(128), nullable=False)
        rack_id = Column(String(60), ForeignKey('racks.id'))
        subrack_id = Column(String(60), ForeignKey('subracks.id'))
        public = Column(Boolean, default=True)
        reviews = relationship("Review", backref="resource")
        
        __mapper_args__ = {
            'polymorphic_identity': 'resource'
        }


    else:
        title = ""
        description = ""
        rack_id = ""
        public = False

    def __init__(self, *args, **kwargs):
        """ Instantiate Object """
        super().__init__(*args, **kwargs)

class Video(Resource):
    """
    Define video resources table for video contents
    """
    if storage_type == 'db':
        __tablename__ = 'videos'
        id = Column(String(60), ForeignKey('resources.id'), primary_key=True)
        description = Column(String(1024), nullable=False)
        video_url = Column(String(255), nullable=False)
        source_type = Column(String(30), default='URL')

class Image(Resource):
    """
    Define Image resources table for Image contents
    """

    if storage_type == 'db':
        __tablename__ = 'images'
        id = Column(String(60), ForeignKey('resources.id'), primary_key=True)
        description = Column(String(1024), nullable=False)
        image_url = Column(String(255), nullable=False)
        source_type = Column(String(30), default='URL')

class Text(Resource):
    """
    Define Text resourcestable for text contents
    """

    if storage_type == 'db':
        __tablename__ = 'texts'
        id = Column(String(60), ForeignKey('resources.id'), primary_key=True)
        content = Column(Text)
