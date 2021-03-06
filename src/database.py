import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = os.environ.get('DATABASE_URL')
if url:
    url = url.replace('postgres', 'postgresql')
else:
    url = 'sqlite:///app.db'

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
