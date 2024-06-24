import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'LD1OHNrAoIsdusrimjV7aoKhn/ZqdEOTtj8RDm+5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://logs:Kushwaha1987@localhost/logs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

