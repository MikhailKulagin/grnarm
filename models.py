from datetime import datetime, date
from pydantic import BaseModel
from pydantic.fields import Optional


class Launch(BaseModel):
    mission_name: Optional[str]
    launch_date_utc: Optional[datetime]
    details: Optional[str]
    is_tentative: Optional[bool]
    launch_date_local: Optional[datetime]
    launch_date_unix: Optional[datetime]
    launch_success: Optional[bool]
    launch_year: Optional[str]
    mission_name: Optional[str]
    static_fire_date_unix: Optional[datetime]
    static_fire_date_utc: Optional[datetime]
    tentative_max_precision: Optional[str]
    upcoming: Optional[bool]
    tstamp: Optional[datetime]

    class Config:
        validate_assignment = True
        orm_mode = True


class Mission(BaseModel):
    name: Optional[str]
    description: Optional[str]
    manufacturers: Optional[str]
    twitter: Optional[str]
    website: Optional[str]
    wikipedia: Optional[str]
    tstamp: Optional[datetime]

    class Config:
            validate_assignment = True
            orm_mode = True


class Rocket(BaseModel):
    name: Optional[str]
    description: Optional[str]
    active: Optional[bool]
    boosters: Optional[int]
    company: Optional[str]
    cost_per_launch: Optional[int]
    country: Optional[str]
    first_flight: Optional[date]
    stages: Optional[int]
    success_rate_pct: Optional[int]
    type: Optional[str]
    wikipedia: Optional[str]
    tstamp: Optional[datetime]

    class Config:
        validate_assignment = True
        orm_mode = True


class DefaultResponse(BaseModel):
    result: bool


class TotalResponse(BaseModel):
    LaunchTable: int
    MissionTable: int
    RocketTable: int
