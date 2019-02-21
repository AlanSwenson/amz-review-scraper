import os

from environs import Env

env = Env()
env.read_env()


def create_config_obj(env_setting):
    new_config = Config()
    with env.prefixed(env_setting):
        new_config.SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
        new_config.DEBUG = env.bool("DEBUG", default=False)
        new_config.TESTING = env.bool("TESTING", default=False)
    return new_config


# proxies
proxies = {"http": env.str("http"), "https": env.str("https")}

# TODO: create a function that randomly selects through a list of headers
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
}

# "y" switches output files on, either html of json or both
html_output_file_switch = "n"
json_output_file_switch = "n"


class Config(object):
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = env.str(
        "SQLALCHEMY_DATABASE_URI", default=env.str("DEV_SQLALCHEMY_DATABASE_URI")
    )
    # SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-S3 settings
    FLASKS3_BUCKET_NAME = env.str("FLASKS3_BUCKET_NAME")
    FLASKS3_CDN_DOMAIN = env.str("FLASKS3_CDN_DOMAIN")
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    # Flask Settings
    SECRET_KEY = env.str("FLASK_SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = False
    SECURITY_PASSWORD_SALT = env.str("SECURITY_PASSWORD_SALT")
    # JWT Settings
    JWT_SECRET_KEY = env.str("FLASK_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False
    WTF_CSRF_ENABLED = False
    # mail settings
    MAIL_SERVER = env.str("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # email authentication
    MAIL_USERNAME = env.str("MAIL_USERNAME")
    MAIL_PASSWORD = env.str("MAIL_PASSWORD")
    # mail accounts
    MAIL_DEFAULT_SENDER = env.str("MAIL_DEFAULT_SENDER")


DevelopmentConfig = create_config_obj("DEV_")
TestingConfig = create_config_obj("TESTING_")
ProductionConfig = create_config_obj("PROD_")
