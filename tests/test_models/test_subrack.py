#!/usr/bin/python3
"""
Defines test for Resource
"""

from models.resource import Resource
from models import storage, storage_type
from models.user import User
from models.library import Library
from models.rack import Rack
from models.rack import Subrack
import unittest


class TestSubrack(unittest.TestCase):
    """
    Tests for Resource class
    """

    if storage_type == 'db':
        user = User(**{
            'firstname': 'John',
            'lastname': 'Keshy',
            'password': 'isbiqoeubfbe',
            'email': 'keshman@usource.com'
        })

        library = Library(**{'name': user.lastname + user.id[-5:],
                             'user_id': user.id
                             })
        rack = Rack(**{
            'name': 'dev_rack',
            'library_id': library.id,
            'description': 'This is a rack with sub rack'
            })

        subrack = Subrack(**{
            'name': 'dev_rack',
            'library_id': library.id,
            'description': 'This is a sub rack',
            'rack_id': rack.id
            })
        resource = Resource(**{
            'title': 'Development resource',
            'description': 'A reesource in a subrack',
            'public': True,
            'subrack_id': subrack.id,
            'content_type': 'link',
            'content': 'https://github.com/Pius-aaron04/Usourceful'
            })
        user.save()
        library.save()
        rack.save()
        subrack.save()


        def test_attributes(self):
            """
            tests attributes.
            """

            self.assertIsInstance(self.resource.title, str)
            self.resource.save()
            self.assertEqual(self.rack.subracks[0], self.subrack)
            self.assertEqual(self.subrack.parent_rack, self.rack)
