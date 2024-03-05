#!/usr/bin/python3
"""
Defines test for Resource
"""

from models.resource import Resource, Video, Image, Text
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


class TestVideoResource(TestResource):
    """
    Tests Video content class.
    This will test the class attributes, and relations
    """

    if storage_type == 'db':
        video = Video(**{
            'title': 'Development resource',
            'description': 'I just dey develop am chill',
            'public': True,
            'rack_id': TestResource.rack.id,
            'source_type': 'URL',
            'video_url': 'https://github.com/Pius-aaron04/Usourceful'
            })

        video1 = Video(**{
            'title': 'Django Tutorial',
            'description': 'A video for Django tutorial' +
                           'for Intermediate devs.',
            'public': True,
            'rack_id': TestResource.rack.id,
            'source_type': 'URL',
            'video_url': 'https://youtu.be/rHux0gMZ3Eg?si=jOwIjEh8TCn2ARsP'
            })

        video.save()
        video1.save()

    def test_attributes(self):
        """
        test for attributes
        """

        # tests for resource to rack link
        self.assertEqual(self.video.rack, self.rack)

        self.assertIsInstance(self.video, Video)
        self.assertIsInstance(self.video.reviews, list)
        self.assertEqual(self.video.source_type, 'URL')
        self.assertEqual(self.video1.public, True)


class TestImage(TestResource):
    """Tests image class"""

    image = Image(**{
            'title': 'Django Tutorial',
            'description': 'A video for Django tutorial' +
                           ' for Intermediate devs.',
            'public': True,
            'rack_id': TestResource.rack.id,
            'source_type': 'URL',
            'image_url': 'https://youtu.be/rHux0gMZ3Eg?si=jOwIjEh8TCn2ARsP'
            })

    image.save()

    def test_attributes(self):
        """Tests attributes"""

        self.assertIsInstance(self.image, Image)
        self.assertIsInstance(self.image.rack, Rack)


class TestText(TestResource):
    """
    Tests Text content class
    """

    text = Text(**{
            'title': 'Django Tutorial',
            'description': 'A note on Django ORM.',
            'public': True,
            'rack_id': TestResource.rack.id,
            'content': 'INTRODUCTION: Django framework is web framework\
            \nthat offers bunch of capabilities.'
        }
    )
    text.save()

    def test_attributes(self):
        """ Tests Test instance attributes."""

        self.assertIsInstance(self.text.content, str)
