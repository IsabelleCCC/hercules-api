from sqlalchemy import Column, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from infrastructure.configs.database import Base

class MuscleGroupByDate(Base):
    __tablename__ = 'muscle_group_by_date'
    __table_args__ = {'info': dict(is_view=True)}

    user_id = Column(Integer, primary_key=True)
    muscle_group = Column(String, primary_key=True)
    count = Column(Integer, primary_key=True)
    week_of_month = Column(String, primary_key=True)
    orderby = Column(String, primary_key=True)
