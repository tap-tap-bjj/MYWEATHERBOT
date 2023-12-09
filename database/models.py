from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, \
    create_engine, DateTime, BigInteger
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    reports = relationship('WeatherReport', backref='report', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.tg_id

class WeatherReport(Base):
    __tablename__ = 'WeatherReports'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now, nullable=False)
    temp = Column(Integer, nullable=False)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)

    def __repr__(self):
        return self.city


