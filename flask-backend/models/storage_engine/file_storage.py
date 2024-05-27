#!/usr/bin/python3

"""
Defines file storage engine
"""

import json
from models.library import Library
from models.rack import Rack
from models.sub_rack import Subrack
from models.resource import Resource
from models.review import Review
from models.recommendation import Recommendation
from models.user import User


class FileStorage:
    """
    File Storage to store and manipulate Json data
    """

    __objects = {}
    __file_path = 'datafile.json'

    def __init__(self):
        """Initializes Storage object"""

        self.classes = {
            'User': User,
            'Library': Library,
            'Rack': Rack,
            'Subrack': Subrack,
            'Resource': Resource,
            'Recommendation': Recommendation,
            'Review': Review
        }

    def new(self, obj):
        """
        Adds new data object to storage cache
        """

        if obj not in self.__objects.values():
            self.__objects['{}.{}'.format(
                obj.to_dict()['__class__'], obj.id)] = obj

    def all(self, cls=None):
        """
        Retrives all data objects in the stored in the storage
        """

        # Retrives data if data class is specified
        if cls:
            all_objects = {}
            classname = cls.__name__
            for key, obj in self.__objects.items():
                if classname == obj.to_dict()['__class__']:
                    all_objects[key] = obj
            return all_objects

        return self.__objects

    def save(self):
        """
        saves json data to the data

        sample:
        {
            {
                id: g7wg8-nidv8-8w3b8s-b83b8s9-niksu,
                created_at: '2024-02-28T07:08:41.102394'
                updated_at: '2024-02-28T07:09:23.239423'
                '__class__': 'User',
                'name': 'Pius Aaron'
            },

            {
                'id': 8usu38-ibiwb-i82b-9938-98unisk9,
                'created_at': '2024-02-28T07:08:41.102394',
                'title': 'Sysadmin',
                'content': 'https://drive.google.com/my_drive/sysadmin'
            }
            ...

        }
        """

        with open(self.__file_path, encoding='utf-8', mode='w') as json_file:
            data = [obj.to_dict() for obj in self.__objects.values()]
            json.dump(data, json_file)

    def reload(self):
        """
        Loads data from the storage
        """

        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as\
                                                                json_file:
                data = json.load(json_file)

            # creates a dictionary of objects with individual object attribute
            self.__objects = {'{}.{}'.format(value['__class__'], value['id']):
                              self.classes[value['__class__']](**value)
                              for value in data}
        except Exception as e:
            print(e)

    def get(self, cls, id):
        """
        fetches a particular object by its id
        """

        if cls in self.classes.values():
            return self.__objects\
                    .get('{}.{}'.format(cls.__class__.__name__, id), None)

    def delete(self, obj):
        """
        Removes data object from storage.
        """

        key = obj.to_dict()['__class__'] + '.' + obj.id

        if key in self.__objects:
            del self.__objects[key]
