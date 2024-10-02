import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/media/avatar/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER', 'Shahzod008')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Shahzod2008')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5432)
    DB = os.environ.get('POSTGRES_DB', 'db')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SECRET_KEY = 'fefrl;4wR$#%T^%$%^E$W%R#T%$HgrfwedwF$#FREBfreg4geRGNTYJ$%HEWY$GSFDBTYNU^MK%^$UE%R$#d'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
