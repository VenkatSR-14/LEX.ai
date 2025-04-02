import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://pruthvi1405:Poojan123@db:5432/documents_db')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
