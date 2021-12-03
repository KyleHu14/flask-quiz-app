import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # If there exists a environment variable, use that, otherwise use the default
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never_guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False