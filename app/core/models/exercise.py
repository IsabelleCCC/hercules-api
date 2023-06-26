from sqlalchemy import Column, Integer, String
from infrastructure.configs.database import Base

# Define the models
class Exercise(Base):
    __tablename__ = 'exercise'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
