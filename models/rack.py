"""
Defines the rack class for rack objects.
"""
from models.base_model import BaseModel
from os import getenv
from sqlachemy import Column, String, Boolean
from sqlachemy.orm import relationship


class Rack(BaseModel):
    """
    Defines Rack objects
    """

    if getenv('USOURCE_STORAGE') == 'db':
        __tablename__ = 'racks'
        name = Column(String(128), nullable=False)
        description = Column(String(255), nullable=False)
        library_id = Column(String(60), nullable=False)
        resources = relationship("Resource", backref="racks")

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
