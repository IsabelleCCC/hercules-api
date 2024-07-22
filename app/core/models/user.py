from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.configs.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(9), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
