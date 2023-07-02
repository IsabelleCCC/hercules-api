from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

# Define the models


class ExerciseWorkoutPlan(Base):
    __tablename__ = 'exerciseworkoutplan'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercise.id'), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey(
        'workoutplan.id'), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    combination = Column(Integer, ForeignKey('exerciseworkoutplan.id'))

    exercise = relationship('Exercise', backref='workout_plans')
    sub_exercises = relationship('ExerciseWorkoutPlan', backref='parent', remote_side=[id])
    workout_plan = relationship('WorkoutPlan', back_populates='exercises_workout_plan')
