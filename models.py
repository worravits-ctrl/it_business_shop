from datetime import datetime
from sqlalchemy import (Column, Integer, String, Date, DateTime, Float, Text, Boolean)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(20), default='user')  # 'admin' or 'user'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    category = Column(String(120), nullable=False)
    description = Column(Text, default='')
    amount = Column(Float, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')
