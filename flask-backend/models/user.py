#!/usr/bin/python3
""" Defines User model class definition"""

from models.base_model import BaseModel, Column, String, Base
from decouple import config
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Defines User model."""

    if config('USOURCE_STORAGE') == 'db':
        __tablename__ = 'users'
        firstname = Column(String(35), nullable=False)
        lastname = Column(String(35), nullable=False)
        username = Column(String(30), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        recommendations = relationship("Recommendation", backref="user")
        library = relationship("Library", backref="user", uselist=False, cascade="all, delete-orphan")

    else:
        firstname = ""
        lastname = ""
        password = ""
        email = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from api.v1.app import bcrypt

        self.password = bcrypt.generate_password_hash(password=self.password)

    def to_dict(self):
        """returns a dictionary of attributes."""
        time = '%Y-%m-%dT%H:%M:%S.%f'

        attributes = self.__dict__.copy()
        attributes['__class__'] = self.__class__.__name__
        del attributes['password']
        attributes['library_id'] = self.library.id

        if 'created_at' in attributes:
            attributes['created_at'] = attributes['created_at'].strftime(time)
        if 'updated_at' in attributes:
            attributes['updated_at'] = attributes['updated_at'].strftime(time)
        if '_sa_instance_state' in attributes:
            del attributes['_sa_instance_state']
        return attributes
