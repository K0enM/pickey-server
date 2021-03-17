import os
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = os.getenv("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class ProductionConfig(Config):
  DEBUG = False
