from sqlalchemy import Column, DateTime, Integer, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

class Workout(Base):
    __tablename__ = 'workout'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    workout_exercise_id = Column(Integer, ForeignKey('exerciseworkoutplan.id'), nullable=False)
    reps = Column(Integer)
    max_weight = Column(DECIMAL(5, 2))
    workout_exercise = relationship("ExerciseWorkoutPlan")
    Index('Workout_fk_WorkoutExercise_idx', workout_exercise_id)
