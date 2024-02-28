"""
Initializes Models.
Starts the based on specified storage type via environment varaible storage engine
"""

from os import getenv

storage_type = getenv('USOURCE_STORAGE')
if storage_type == 'db':
    from models.storage_engine.file_storage import DBStorage
    storage = DBStorage()

else:
    from models.storage_engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
