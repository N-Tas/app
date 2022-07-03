from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib


server = "polynomial.database.windows.net"
database = "polynomial"
username = "nAzZo"
password = "Dummy123"

driver = '{ODBC Driver 17 for SQL Server}'

odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()