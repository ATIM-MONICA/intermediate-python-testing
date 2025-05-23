from datetime import timedelta

class Config:
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/e_commerce_db'
     JWT_SECRET_KEY = "exam" 
     JWT_EXPIRATION_DELTA = timedelta(minutes=10)
