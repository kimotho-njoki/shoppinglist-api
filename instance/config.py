import os

class Config(object):
    """
    Base configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "my_secret_random_key"
    SQLALCHEMY_DATABASE_URI = 'postgres://wwdrkcouxhqeos:6406b0bf71c853c331789e57a567f64464f6769db4c9ea00b2adb33279954f5e@ec2-54-204-41-80.compute-1.amazonaws.com:5432/d12jlnt39247j7'

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
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/shoplistapi_db'
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
