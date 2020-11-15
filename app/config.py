import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _build_uri(
    user: str,
    password: str,
    host: str,
    port: int,
    db: str,
) -> str:
    return f'mysql://{user}:{password}@{host}:{port}/{db}'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT'))
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = _build_uri(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        db=MYSQL_DATABASE,
    )
    OER_APP_ID = os.getenv('OER_APP_ID')


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
