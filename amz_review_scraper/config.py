import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


# Set environment :: "development" or "production"
env_setting = "development"


# import .env variables for DB connection
if env_setting == "development":
    POSTGRES_USER = get_env_variable("DEV_POSTGRES_USER")
    POSTGRES_PW = get_env_variable("DEV_POSTGRES_PW")
    POSTGRES_URL = get_env_variable("DEV_POSTGRES_URL")
    POSTGRES_DB = get_env_variable("DEV_POSTGRES_DB")
elif env_setting == "production":
    POSTGRES_USER = get_env_variable("PROD_POSTGRES_USER")
    POSTGRES_PW = get_env_variable("PROD_POSTGRES_PW")
    POSTGRES_URL = get_env_variable("PROD_POSTGRES_URL")
    POSTGRES_DB = get_env_variable("PROD_POSTGRES_DB")

# proxies
http = get_env_variable("http")
https = get_env_variable("https")
proxies = {"http": http, "https": https}

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
}

# DB
DB_URL = create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)

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
    # ...
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = FLASK_SECRET_KEY
    FLASKS3_BUCKET_NAME = S3_NAME
    FLASKS3_CDN_DOMAIN = S3_CDN
    AWS_ACCESS_KEY_ID = AWS_KEY
    AWS_SECRET_ACCESS_KEY = AWS_SECRET
    # FLASKS3_DEBUG = True
