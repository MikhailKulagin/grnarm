from typing import List, Union
import sys, inspect
from sqlalchemy.future import select

import models
from database.db_models import LaunchTable, MissionTable, RocketTable


class DbClient:
    def __init__(self,
                 session
                 ):
        self.session = session

    async def insert_data(self,
                          data: Union[List[models.Mission], List[models.Launch], List[models.Rocket]],
                          db_model: Union[MissionTable, LaunchTable, RocketTable]):
        new_items = []
        for item in data:
            if 'launch_date_utc' in dir(item):
                # TODO: Подумать. Graph возвращает строку с датой, которую не получается инсертить
                item.launch_date_utc = item.launch_date_utc.utcnow()
            new_items.append(db_model(**item.dict()))
        self.session.add_all(new_items)
        await self.session.flush()
        await self.session.commit()

    async def add_launches(self, launches: List[models.Launch]):
        await self.insert_data(launches, LaunchTable)

    async def add_rockets(self, rockets: List[models.Rocket]):
        await self.insert_data(rockets, RocketTable)

    async def add_missions(self, missions: List[models.Mission]):
        await self.insert_data(missions, MissionTable)

    async def select_totals(self):
        count_res = {}
        for t_name, obj in inspect.getmembers(sys.modules["database.db_models"]):
            if t_name.endswith("Table"):
                q = select(obj.id)
                res = await self.session.execute(q)
                curr = res.scalars()
                count = len([_ for _ in curr])
                count_res[t_name] = count
        return count_res
