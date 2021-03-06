from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, SmallInteger, Text, Time, func, or_, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased, relationship, sessionmaker
import bcrypt

Base = declarative_base()
Session = sessionmaker()

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    key = Column(String(256))
    sensors = relationship("Sensor")
    _password = Column(String(128))

    @hybrid_property
    def password(self):
        return self._password

    def set_password(self, plaintext):
        salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(plaintext.encode('utf8'), salt)

    def is_correct_password(self, plaintext):
        password = self._password
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf8')
        if isinstance(password, str):
            password = password.encode('utf8')
        return bcrypt.checkpw(plaintext, password)

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    modelname =  Column(String(256))
    station_id = Column(Integer, ForeignKey('stations.id'))
    Station = relationship("Station", back_populates="sensors")
    measurements = relationship("Measurement")
    MeasurementType_id = Column(Integer, ForeignKey('types.id'))
    MeasurementType = relationship("MeasurementType", back_populates="sensors")

class MeasurementType(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), unique=True)
    unit = Column(String(256))
    sensors = relationship("Sensor")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    Sensor = relationship(Sensor, back_populates="measurements")
    datetime = Column(DateTime)
    lon = Column(Float)
    lat = Column(Float)
