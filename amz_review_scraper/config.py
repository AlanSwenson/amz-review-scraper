import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


# import .env variables for DB connection
# TODO: Unify these ENV variables by pulling from different dot files
def get_env_db_url(env_setting):
    if env_setting == "development":
        POSTGRES_USER = get_env_variable("DEV_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("DEV_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("DEV_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("DEV_POSTGRES_DB")
    elif env_setting == "testing":
        POSTGRES_USER = get_env_variable("TESTING_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("TESTING_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("TESTING_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("TESTING_POSTGRES_DB")
    elif env_setting == "production":
        POSTGRES_USER = get_env_variable("PROD_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("PROD_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("PROD_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("PROD_POSTGRES_DB")

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")


# proxies
http = get_env_variable("http")
https = get_env_variable("https")
proxies = {"http": http, "https": https}

# TODO: create a function that randomly selects through a list of headers
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
}


# Flask setup
FLASK_SECRET_KEY = get_env_variable("FLASK_SECRET_KEY")
S3_NAME = get_env_variable("FLASKS3_BUCKET_NAME")
S3_CDN = get_env_variable("FLASKS3_CDN_DOMAIN")

# aws credentials
AWS_KEY = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET = get_env_variable("AWS_SECRET_ACCESS_KEY")

# "y" switches output files on, either html of json or both
html_output_file_switch = "n"
json_output_file_switch = "n"


class Config(object):
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-S3 settings
    FLASKS3_BUCKET_NAME = S3_NAME
    FLASKS3_CDN_DOMAIN = S3_CDN
    AWS_ACCESS_KEY_ID = AWS_KEY
    AWS_SECRET_ACCESS_KEY = AWS_SECRET
    # Flask Settings
    SECRET_KEY = FLASK_SECRET_KEY
    # SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = False
    # FLASKS3_DEBUG = True
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    DEBUG = False
    TESTING = False
