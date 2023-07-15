import os

class Config:
    """ basic configurations."""
    DEBUG = False
    PORT = os.environ.get('PORT') or 5000
    ENV = os.environ.get('ENV')
    FLASK_APP = os.environ.get('APP_NAME')

    SQLALCHEMY_DATABASE_URI = "mysql://root:@127.0.0.1/ai_analysis"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class development(Config):
    """development configuration """
    DEBUG = True


class production(Config):
    """ production configuration """
    PORT = os.environ.get('PORT') or 8080
