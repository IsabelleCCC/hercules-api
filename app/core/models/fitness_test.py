from sqlalchemy import Column, Integer, DateTime, DECIMAL, Text, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base


# Define the models
class FitnessTest(Base):
    __tablename__ = 'fitnesstest'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    weight = Column(DECIMAL(5,2), nullable=False)
    body_fat = Column(DECIMAL(4,2))
    chest = Column(DECIMAL(5,2))
    right_arm_contr = Column(DECIMAL(5,2))
    left_arm_contr = Column(DECIMAL(5,2))
    hip = Column(DECIMAL(5,2))
    right_arm_relax = Column(DECIMAL(5,2))
    left_arm_relax = Column(DECIMAL(5,2))
    abdomen = Column(DECIMAL(5,2))
    waist = Column(DECIMAL(5,2))
    right_forearm = Column(DECIMAL(5,2))
    left_forearm = Column(DECIMAL(5,2))
    right_thigh = Column(DECIMAL(5,2))
    left_thigh = Column(DECIMAL(5,2))
    scapular = Column(DECIMAL(5,2))
    right_calf = Column(DECIMAL(5,2))
    left_calf = Column(DECIMAL(5,2))
    observations = Column(Text)
    user = relationship('User', backref='fitness_tests')
