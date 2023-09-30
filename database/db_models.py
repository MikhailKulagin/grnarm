import sqlalchemy
from sqlalchemy import BigInteger, Column, DateTime, String, UniqueConstraint, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

metadata = sqlalchemy.MetaData()
Base = declarative_base()


class LaunchTable(Base):
    __tablename__ = "t_launches"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    mission_name = Column(String(50))
    launch_date_utc = Column(DateTime)
    details = Column(String(4000))
    is_tentative = Column(Boolean)
    launch_date_local = Column(DateTime)
    launch_date_unix = Column(DateTime)
    launch_success = Column(Boolean)
    launch_year = Column(String(10))
    mission_name = Column(String(50))
    static_fire_date_unix = Column(DateTime)
    static_fire_date_utc = Column(DateTime)
    tentative_max_precision = Column(String(50))
    upcoming = Column(Boolean)
    tstamp = Column(DateTime)
    __table_args__ = (UniqueConstraint("mission_name", name='uniqLaunchTable'), )


class MissionTable(Base):
    __tablename__ = "t_missions"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(4000))
    manufacturers = Column(String(50))
    twitter = Column(String(50))
    website = Column(String(50))
    wikipedia = Column(String(50))
    tstamp = Column(DateTime)
    __table_args__ = (UniqueConstraint("name", name='uniqMissionTable'), )


class RocketTable(Base):
    __tablename__ = "t_rockets"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(4000))
    active = Column(Boolean)
    boosters = Column(BigInteger)
    company = Column(String(50))
    cost_per_launch = Column(BigInteger)
    country = Column(String(50))
    first_flight = Column(Date)
    stages = Column(BigInteger)
    success_rate_pct = Column(BigInteger)
    type = Column(String(50))
    wikipedia = Column(String(50))
    tstamp = Column(DateTime)
    __table_args__ = (UniqueConstraint("name", name='uniqRocketTable'), )
