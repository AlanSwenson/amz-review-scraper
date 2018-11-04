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


# This is pulling in a dict and making it a string
# proxies
http = get_env_variable('http')
https = get_env_variable('https')
proxies = {'http' : http, 'https' : https}


DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
