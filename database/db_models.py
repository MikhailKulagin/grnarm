import sqlalchemy
from sqlalchemy import BigInteger, Column, DateTime, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

metadata = sqlalchemy.MetaData()
Base = declarative_base()


class LaunchTable(Base):
    __tablename__ = "t_launches"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mission_name = Column(String(50))
    launch_date_utc = Column(DateTime)
    __table_args__ = (UniqueConstraint("mission_name", name='uniqLaunchTable'), )


class MissionTable(Base):
    __tablename__ = "t_missions"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(4000))
    __table_args__ = (UniqueConstraint("name", name='uniqMissionTable'), )


class RocketTable(Base):
    __tablename__ = "t_rockets"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(4000))
    __table_args__ = (UniqueConstraint("name", name='uniqRocketTable'), )
