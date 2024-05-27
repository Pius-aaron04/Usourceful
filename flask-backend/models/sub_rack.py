#!/usr/bin/python3
"""
Defines sub-racks.
"""
from models.rack import String, Column, ForeignKey, Base, BaseModel, Boolean
from sqlalchemy.orm import relationship
from decouple import config


class Subrack(BaseModel, Base):
    """
    Sub racks for branched racks.
    """

    if config('USOURCE_STORAGE') == 'db':
        __tablename__ = 'subracks'
        name = Column(String(128), nullable=False)
        description = Column(String(255), nullable=False)
        library_id = Column(String(60), ForeignKey('libraries.id'),
                            nullable=False)
        public = Column(Boolean, default=True, nullable=False)
        resources = relationship("Resource", backref="subrack")

        rack_id = Column(String(60), ForeignKey('racks.id'), nullable=False)

    else:
        rack_id = ""

    def __init__(self, *args, **kwargs):

        """
        Initializes class

        param 1: non keyword args
        param 2: for keyword args
        """

        super().__init__(*args, **kwargs)
