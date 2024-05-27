"""
Initializes Models.
Starts the based on specified storage type via environment variable
storage engine
"""

from decouple import config
import os

storage_type = config('USOURCE_STORAGE')
if storage_type == 'db':
    from models.storage_engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from models.storage_engine.file_storage import FileStorage
    storage = FileStorage()


storage.reload()

# creates directory for all users
BASEDIR = os.path.join(os.path.expanduser('~'), 'usource')
if not os.path.exists(BASEDIR):
    os.makedirs(BASEDIR)
