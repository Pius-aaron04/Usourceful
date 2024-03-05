#!/usr/bin/python3
"""
Defines test for Resource
"""

from models.resource import Resource
from models import storage, storage_type
from models.user import User
from models.library import Library
from models.rack import Rack
import unittest


class TestResource(unittest.TestCase):
    """
    Tests for Resource class
    """

    if storage_type == 'db':
        user = User(**{
            'firstname': 'John',
            'lastname': 'Doe',
            'password': 'isbiqoeubfbe',
            'email': 'JohnJohndoe@usource.com'
        })

        library = Library(**{'name': user.lastname + user.id[-5:],
                             'user_id': user.id
                             })
        rack = Rack(**{
            'name': 'dev_rack',
            'library_id': library.id,
            'description': 'This is a test rack for development'
            })
        resource = Resource(**{
            'title': 'Development resource',
            'description': 'I just dey develop am chill',
            'public': True,
            'rack_id': rack.id,
            'content_type': 'link',
            'content': 'https://github.com/Pius-aaron04/Usourceful'
            })
        user.save()
        library.save()
        rack.save()


        def test_attributes(self):
            """
            tests attributes.
            """

            self.assertIsInstance(self.resource.title, str)
            self.resource.save()
