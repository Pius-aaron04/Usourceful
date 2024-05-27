#!/usr/bin/python3
"""
Defines review table
"""
from models.base_model import BaseModel, Column, String, Base
from decouple import config
from sqlalchemy import ForeignKey 

storage_type = config('USOURCE_STORAGE')


class Review(BaseModel, Base):
    """
    Defines Review table/class
    """

    if storage_type == 'db':
        __tablename__ = 'reviews'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)

        __mapper_args__ = {
                'polymorphic_identity': 'review'
                }
    else:
        user_id = ""
        resource_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes class object
        """
        super().__init__(*args, **kwargs)



class ResourceReview(Review):
    """
    Defines reviews for Resource related reviews
    """

    if storage_type == 'db':
        __tablename__ = 'resource_reviews'
        id = Column(String(60), ForeignKey('reviews.id'), primary_key=True)
        resource_id = Column(String(60), ForeignKey('resources.id'),
                             nullable=False)


class RackReview(Review):
    """
    Defines Rack related reviews
    """

    if storage_type == 'db':
        __tablename__ = 'rack_reviews'
        
        id = Column(String(60), ForeignKey('reviews.id'), primary_key=True)
        rack_id = Column(String(60), ForeignKey('racks.id'))

