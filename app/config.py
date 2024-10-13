import os



class Config():
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/media/avatar/'
    UPLOAD_PATH_PUBLICATION_IMAGE = '/media/publication_image/'
    UPLOAD_PATH_PUBLICATION_VIDEO = '/media/publication_video/'
    UPLOAD_PATH_PUBLICATION_AUDIO = '/media/publication_audio/'
    SERVER_PATH_AVATAR = ROOT + UPLOAD_PATH
    SERVER_PATH_PUBLICATION_IMAGE = ROOT + UPLOAD_PATH_PUBLICATION_IMAGE
    SERVER_PATH_PUBLICATION_VIDEO = ROOT + UPLOAD_PATH_PUBLICATION_VIDEO
    SERVER_PATH_PUBLICATION_AUDIO = ROOT + UPLOAD_PATH_PUBLICATION_AUDIO

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'shahzod9966636043@gmail.com'
    MAIL_DEFAULT_SENDER = 'shahzod9966636043@gmail.com'
    MAIL_PASSWORD = 'mbqv vqnk yvno ijqh'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


    USER = os.environ.get('POSTGRES_USER', 'Shahzod008')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Shahzod2008')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5432)
    DB = os.environ.get('POSTGRES_DB', 'db')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SECRET_KEY = 'fefrl;4wR$#%T^%$%^E$W%R#T%$HgrfwedwF$#FREBfreg4geRGNTYJ$%HEWY$GSFDBTYNU^MK%^$UE%R$#d'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
