#!/usr/bin/python3

"""
Defines the rack class for rack objects.
"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.resource import Resource
from models.sub_rack import Subrack


class Rack(BaseModel, Base):
    """
    Defines Rack objects
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = 'racks'
        name = Column(String(128), nullable=False)
        description = Column(String(255), nullable=False)
        library_id = Column(String(60), ForeignKey('libraries.id'),
                            nullable=False)
        public = Column(Boolean, default=True, nullable=False)
        resources = relationship(Resource, backref="rack")
        subracks = relationship(Subrack, backref="parent_rack")

    else:
        name = ""
        description = ""
        library_id = ""
        resources = []

    def __init__(self, *args, **kwargs):
        """
        Initialize class with specified parameters

        param 1: non named arguments
        param 2: keyword arguments for passing in data attributes
        """

        super().__init__(*args, **kwargs)
