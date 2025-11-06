import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True
    TESTING = False

    # Flask app configuration
    FLASK_APP = 'app.py'
    FLASK_ENV = 'development'

    # URL configuration for accessing the website
    BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:5000'
    API_BASE_URL = os.environ.get('API_BASE_URL') or 'https://localhost:8000/api'

    # Static files
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
