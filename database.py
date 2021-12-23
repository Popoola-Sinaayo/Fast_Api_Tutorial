from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

engine = create_engine("postgresql://postgres:Prayer1020@localhost/FastApi",
echo = True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)