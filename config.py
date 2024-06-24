import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'LD1OHNrAoIsdusrimjV7aoKhn/ZqdEOTtj8RDm+5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://logs:Kushwaha1987@localhost/logs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = os.environ.get('AKIA47CRY4FXQJTGZYHJ')
    AWS_SECRET_ACCESS_KEY = os.environ.get('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')
    AWS_S3_BUCKET = os.environ.get('s3tochlogtest')

