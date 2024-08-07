from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

# Define the models
class Exercise(Base):
    __tablename__ = 'Exercise'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    muscle_group = Column(String(45), nullable=False)
