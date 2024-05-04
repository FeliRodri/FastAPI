from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" while True:   
    
    try:
        with psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='xxxx', row_factory=dict_row) as conn:
    
            with conn.cursor() as cur:
                print("Database connection was sucessfull!!")
            break
                
    except Exception as error:
                print("Connecting to database failed")
                print("Error: ", error)
                time.sleep(3)  """
    
 
# def get_database_connection():
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='xxxx', row_factory=dict_row)
#         return conn
#     except psycopg.OperationalError as e:
#         # Manejar el error de conexión
#         print("Error de conexión a la base de datos:", e)
#         time.sleep(3)
#         return None
