import os

class Config(object):
    """
    Base configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "my_secret_random_key"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2.9.0.1.@localhost/shoplistapi_db'

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2.9.0.1.@localhost/shoplistapi_db'
    DEBUG = True

class StagingConfig(Config):
    """
    Staging configurations
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
