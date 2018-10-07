from .models import *
# from .views import *
from mongoengine import connect
from .config import DB_NAME, HOSTNAME, PORT
from .app_environment import AppEnvironment

connect(DB_NAME, host=HOSTNAME, port=PORT)