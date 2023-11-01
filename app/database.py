import psycopg2
import time
from psycopg2.extras import RealDictCursor # to also return the column names, and format the output as a dictionary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

username = settings.pg_username
password = settings.pg_password
host = settings.pg_host
port = settings.pg_port
database = settings.pg_database
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Establishing a database connection via psycopg2 (don't need anymore after switching to sqlalchemy orm)
# while True:

#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             port='5433',
#             database='fastapi',
#             user='postgres',
#             password='Jpoy8ethqw',
#             cursor_factory=RealDictCursor
#             )
#         cur = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("Error: ", error)
#         time.sleep(3) # if connection fails, wait for 3 seconds before another attempt