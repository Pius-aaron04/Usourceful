from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.racks import *
from api.v1.views.resources import *
from api.v1.views.library import *
from api.v1.views.users import *
