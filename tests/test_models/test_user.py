#!/usr/bin/python3
"""
Tests User class attributes and mehods
"""
import unittest
from os import getenv
from models.user import User
from datetime import datetime


class TestUser(unittest.TestCase):
    """"
    Class to test user objects
    """

    def test_instantiation(self):
        """
        Test Object creation with or without arguments
        And also test attributes
        """

        if getenv('USOURCE_STORAGE') != 'db':
            user = User()
            self.assertIsInstance(user.to_dict(), dict)
            self.assertIsInstance(user.created_at, datetime)
            self.assertIsInstance(user.updated_at, datetime)
            self.assertEqual(user.to_dict()['__class__'], "User")

            user1 = User(**{'name': 'Pius', 'email': 'piuschbx@gmail.com'})
            self.assertEqual(user1.name, 'Pius')
