from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Server='MSI\SQLEXPRESS'
Database='Fastapi'
Driver1='SQL Server'

Databaseconn=f'mssql://@{Server}/{Database}?driver={Driver1}'

engine=create_engine(Databaseconn)

conn=engine.connect()

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
