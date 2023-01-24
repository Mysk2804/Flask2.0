import atexit
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


PG_DSN = 'postgresql://app:1234@127.0.0.1:5431/advertisement'
engine = create_engine(PG_DSN)
Base = declarative_base(bind=engine)


class AdvertisementModel(Base):

    __tablename__ = 'app_advertisement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    date_of_creation = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)
