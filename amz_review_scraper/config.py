import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# import .env variables for DB connection
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

# proxies
http = get_env_variable("http")
https = get_env_variable("https")
proxies = {"http": http, "https": https}

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
}


DB_URL = "postgresql://{user}:{pw}@{url}/{db}".format(
    user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB
)

FLASK_SECRET_KEY = get_env_variable("FLASK_SECRET_KEY")
S3_NAME = get_env_variable("FLASKS3_BUCKET_NAME")

# "y" switches output files on, either html of json or both
html_output_file_switch = "n"
json_output_file_switch = "n"


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = FLASK_SECRET_KEY
    FLASKS3_BUCKET_NAME = S3_NAME
