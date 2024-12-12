import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password12345'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{BASE_DIR}/instance/tasks.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
