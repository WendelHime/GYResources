import os


class DefaultConfig(object):
    """Default configuration"""
    DEBUG = False
    # Database setting
    DBHOST = '127.0.0.1'
    DBUSER = 'capivara'
    DBPASS = 'test'
    DBPORT = '5432'
    DBNAME = 'green_eyes'
    # Application setting
    # SERVER_NAME = '0.0.0.0:5000'
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    TYPE = 'DEV'
    ELASTICURL = 'http://127.0.0.1:9200'
    SECRET_KEY = 'testing gyresources api'
    IMAGESPATH = os.getcwd()
    EXPIRATION_TOKEN = 600
    # TF Serving server
    TFSHOST = '172.17.0.2'
    TFSPORT = '7000'
    # Email setting
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'green.eyescorporate@gmail.com'
    MAIL_PASSWORD = 'ohhjxhswxjdanxvs'
    WINDOW_SIZE = 28
    CELERY_BROKER_URL = 'amqp://localhost//'
    BROKER_POOL_LIMIT = 200
    THREADS = 4
    CELERYD_CONCURRENCY = 4
    CELERYBEAT_SYNC_EVERY = 300
    BROKER_HEARTBEAT = 300
    BROKER_HEARTBEAT_CHECKRATE = 2.0
    PROJECT_ID = ''
    STORAGE_BUCKET = ''
    JSON_AUTH = ''


class TestConfig(object):
    """Test configuration"""
    # Database setting
    DBHOST = '127.0.0.1'
    DBUSER = 'capivara'
    DBPASS = 'test'
    DBPORT = '5432'
    DBNAME = 'green_eyes'
    # Application setting
    # SERVER_NAME = '0.0.0.0:5000'
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    TYPE = 'TEST'
    ELASTICURL = 'http://127.0.0.1:9200'
    SECRET_KEY = 'testing gyresources api'
    IMAGESPATH = os.getcwd()
    EXPIRATION_TOKEN = 240
    # TF Serving server
    TFSHOST = '172.17.0.2'
    TFSPORT = '7000'
    # Email setting
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'green.eyescorporate@gmail.com'
    MAIL_PASSWORD = 'ohhjxhswxjdanxvs'
    WINDOW_SIZE = 28
    CELERY_BROKER_URL = 'amqp://localhost//'
    BROKER_POOL_LIMIT = 200
    THREADS = 2
    CELERYD_CONCURRENCY = 4
    CELERYBEAT_SYNC_EVERY = 300
    BROKER_HEARTBEAT = 300
    BROKER_HEARTBEAT_CHECKRATE = 2.0
    PROJECT_ID = ''
    STORAGE_BUCKET = ''
    JSON_AUTH = ''
