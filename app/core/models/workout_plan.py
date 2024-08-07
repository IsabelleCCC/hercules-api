from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from infrastructure.configs.database import Base

class WorkoutPlan(Base):
    __tablename__ = 'WorkoutPlan'
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    exercise_plans = relationship('ExercisePlan', back_populates= 'workout_plan', cascade='all, delete', passive_deletes=True)
    user = relationship('User', backref='workout_plans')
