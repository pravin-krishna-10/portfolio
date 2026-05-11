import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'Your-secret-key-change-this-to-later'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir,'static','papers')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB