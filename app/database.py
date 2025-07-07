from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# When using a ORM you need to create a database url that is used to connect to the database. 
# Also make sure you have your SQL driver installed.
# URL FORMAT - 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create dependency - this must come AFTER SessionLocal is defined
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
           
# # connecting to the postgres database using sqlpostgres driver psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='adi62000', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connected to the database successfully!")
#         break
#     except Exception as e:
#         print("Connection to the datavase failed")
#         print("error: ",e)
#         # if connection failed wait for 3 secs and retry.
#         time.sleep(3)