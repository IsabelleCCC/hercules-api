from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import select
from infrastructure.configs.database import Base
from core.models.exercise import Exercise

class ExercisePlan(Base):
    __tablename__ = 'ExercisePlan'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('Exercise.id'), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('WorkoutPlan.id', ondelete='CASCADE'), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    combination = Column(Integer, ForeignKey('ExercisePlan.id'))

    exercise = relationship('Exercise', backref='exercise_plans')
    sub_exercises = relationship('ExercisePlan', backref='parent', remote_side=[id])
    workout_plan = relationship('WorkoutPlan', back_populates='exercise_plans')

    exercise_name = column_property(
        select(Exercise.name).where(Exercise.id == exercise_id).scalar_subquery()
    )
