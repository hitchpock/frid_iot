"""
Класс сотрудник.
"""
from datetime import datetime
from sqlalchemy import Column, Boolean, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()

class IDWorker(Base):
    __tablename__ = 'enter_group'
    id = Column(Integer, primary_key=True)
    uid = Column(String(14), index=True, unique=True)


class Worker(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(64), index=True, unique=True)
    uid = Column(String(14), index=True, unique=True)
    insafe = Column(Boolean, default=False)
    

    def __repr__(self):
        return "<Worker {}>".format(self.fullname)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), index=True)
    dtime = Column(DateTime, index=True, default=datetime.utcnow)
    button = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    lora_id = Column(String(14), index=True, unique=True)
    endtime = Column(DateTime, index=True, default=datetime.utcnow)
