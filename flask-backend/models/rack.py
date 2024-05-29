#!/usr/bin/python3

"""
Defines the rack class for rack objects.
"""
from decouple import config
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.resource import Resource
from models.sub_rack import Subrack


class Rack(BaseModel, Base):
    """
    Defines Rack objects

    Attributes
    ==========

    name: Rack name
    Description: Short description of the Rack object
    library_id: link to user library which Rack belongs
    public: sets visible or invisible for users
    resources: list of all resources link to rack
    subracks: list of children racks

    """

    if config('USOURCE_STORAGE') == 'db':
        __tablename__ = 'racks'
        name = Column(String(128), nullable=False)
        description = Column(String(255), nullable=False)
        library_id = Column(String(60), ForeignKey('libraries.id'),
                            nullable=False)
        public = Column(Boolean, default=True, nullable=False)
        resources = relationship(Resource, backref="rack", cascade="all, delete-orphan")
        subracks = relationship(Subrack, backref="parent_rack", cascade="all, delete-orphan")
        reviews = relationship('RackReview', backref='rack', cascade="all, delete-orphan")

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

    @property
    def num_items(self):
        """
        calculates number of resources in a rack
        """

        return len(self.resources) if self.resources else 0
