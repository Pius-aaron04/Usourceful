#!/usr/bin/python3
"""
Tests User class attributes and mehods
"""
import json
import unittest
from os import getenv
from models.user import User
from datetime import datetime
import models


class TestUser(unittest.TestCase):
    """"
    Class to test user objects
    """
    if models.storage_type != 'db':
        user = User()
        user1 = User(**{'name': 'Pius', 'email': 'piuschbx@gmail.com'})
    else:
        user = User(firstname="Pius", lastname="Aaron",
                    email="pius@usourceful.com", password="kilode_gan_gan")
        user1 = User(**{
            "firstname": "Catherine",
            "lastname": "John",
            "email": "catherine0801@usource.com",
            "password": "uvdajkw839o49fiie0"
            })

    def test_instantiation(self):
        """
        Test Object creation with or without arguments
        And also test attributes
        """


        self.assertIsInstance(self.user.to_dict(), dict)
        # self.assertIsInstance(self.user.created_at, datetime)
        # self.assertIsInstance(self.user.updated_at, datetime)
        self.assertEqual(self.user.to_dict()['__class__'], "User")

        self.assertEqual(self.user1.firstname, 'Catherine')

    def test_methods(self):
        """
        Test User methods
        """

        if models.storage_type != 'db':
            self.user.save()
            with open("datafile.json", 'r') as json_file:
                data = json.load(json_file)
        else:
            self.user.save()
            data = list(models.storage.all().values())

        self.assertTrue(self.user in data)
        self.assertTrue(self.user in models.storage.all(User).values())
        models.storage.delete(self.user)
