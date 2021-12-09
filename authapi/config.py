import os
from .env import setEnvironment

if os.environ.get('ENV') != "PROD":
    #In heroku the variables will be supplied from heroku
    setEnvironment()

SALT = os.environ.get("SALT")
SECRET_KEY = os.environ.get("SECRET_KEY")
#CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
