from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# When using a ORM you need to create a database url that is used to connect to the database. 
# Also make sure you have your SQL driver installed.
# URL FORMAT - 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:adi62000@localhost/fastapi'

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