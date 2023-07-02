from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

# Define the models


class WorkoutPlan(Base):
    __tablename__ = 'workoutplan'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='workout_plans')
    exercises_workout_plan = relationship('ExerciseWorkoutPlan', back_populates='workout_plan')
