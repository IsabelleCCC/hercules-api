from sqlalchemy import Column, DateTime, Integer, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

class ExerciseDone(Base):
    __tablename__ = 'ExerciseDone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reps = Column(Integer)
    max_weight = Column(DECIMAL(5, 2))
    workout_done_id = Column(Integer, ForeignKey('WorkoutDone.id'), nullable=False)
    exercise_plan_id = Column(Integer, ForeignKey('ExercisePlan.id'), nullable=False)

    exercise_plan = relationship('ExercisePlan', backref='exercises_done')
    workout_done = relationship('WorkoutDone', back_populates='exercises_done')
