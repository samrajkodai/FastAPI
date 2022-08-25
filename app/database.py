from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Server='MSI\SQLEXPRESS'
Database='Fastapi'
Driver1='SQL Server'

Databaseconn='postgres://aifhxkcpkmjxls:6861e98a65043b1ebe2f0d58e945195f98736fa4dd3d25d1490e5c7722e753d9@ec2-34-227-135-211.compute-1.amazonaws.com:5432/d723pbmneak647'

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
