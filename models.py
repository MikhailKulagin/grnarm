from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Optional


class Launch(BaseModel):
    mission_name: Optional[str]
    launch_date_utc: Optional[datetime]

    class Config:
        validate_assignment = True
        orm_mode = True


class Mission(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
            validate_assignment = True
            orm_mode = True


class Rocket(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        validate_assignment = True
        orm_mode = True
