from sqlalchemy import Column, DateTime, Integer, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

class WorkoutDone(Base):
    __tablename__ = 'WorkoutDone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    duration = Column(DECIMAL(5,2), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('WorkoutPlan.id'), nullable=False)

    workout_plan = relationship('WorkoutPlan', backref='workouts_done')
    exercises_done = relationship('ExerciseDone', back_populates='workout_done')
