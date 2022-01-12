import datetime
import os

try:
    APP_ENV = str(os.environ["APP_ENV"])
except KeyError:
    APP_ENV = "development"

ROOT = os.path.dirname(os.path.abspath(__file__))


class Config:
    # api
    API_VERSION = "v1"

    # app
    SITE_HTTPS = os.environ.get("SITE_HTTPS") + os.environ.get("API_PORT")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JSON_SORT_KEYS = False

    # jwt
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRES = 3600
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=3600)
    BASIC_CLIENT = os.environ.get("BASIC_CLIENT")
    BASIC_ADMIN = os.environ.get("BASIC_ADMIN")

    # sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 0
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.environ.get("DB_USER", "root"),
        os.environ.get("DB_PASS", "root"),
        os.environ.get("DB_HOST", "localhost"),
        os.environ.get("DB_NAME", "flask_api_template")
    )

    # cache
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "simple")
    if CACHE_TYPE == "redis":
        CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST")
        CACHE_REDIS_PORT = os.environ.get("CACHE_REDIS_PORT")
        CACHE_KEY_PREFIX = SITE_HTTPS

    # aws
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_LOCATION = None
    AWS_BUCKET = None
    AWS_BUCKET_LOCATION = AWS_LOCATION
    AWS_BUCKET_CLOUDFRONT = None

    # kraken
    KRAKEN_API_KEY = os.environ.get("KRAKEN_API_KEY")
    KRAKEN_API_SECRET = os.environ.get("KRAKEN_API_SECRET")
