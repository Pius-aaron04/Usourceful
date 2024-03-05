#!/usr/bin/python3
""" Defines test class for Library class"""
from models import storage, storage_type
import unittest
from models.library import Library
from models.user import User


class TestLibrary(unittest.TestCase):
    """test the Library class."""

    if storage_type != 'db':
        user = User(firstname="John")
        library = Library(name=user.firstname+'.' + user.id[:5],
                          user_id=user.id)

    else:
        user = User(**{
            'firstname': 'Doe',
            'lastname': 'Lanister',
            'email': 'lanisterdoe@usource.com',
            'password': 'lhydbuiai'
            })
        library = Library({
            'user_id': user.id,
            'name': user.firstname + user.id[:5]
            })

    def test_attributes(self):
        """
        test library attributes.
        """

        self.assertIsInstance(self.library.to_dict(), dict)
        if storage_type == 'db':
            self.assertEqual(self.user.library, self.library)
            self.assertIsInstance(self.library.user, User)

    def teardown(self):
        """
        Clean up tests
        """

        self.user.delete()
        self.library.delete()
