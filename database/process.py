from typing import List, Union
import sys, inspect
from sqlalchemy.future import select
from sqlalchemy.dialects.sqlite import insert

from models import Mission, Rocket, Launch
from database.db_models import LaunchTable, MissionTable, RocketTable


class DbClient:
    def __init__(self,
                 session
                 ):
        self.session = session

    async def insert_data(self,
                          data: Union[List[Mission], List[Launch], List[Rocket]],
                          db_model: Union[MissionTable, LaunchTable, RocketTable]):
        new_items = []
        for item in data:
            if 'launch_date_utc' in dir(item):
                # TODO: Убрать костыль. Graph возвращает строку с датой, которую не получается инсертить
                item.launch_date_utc = item.launch_date_utc.utcnow()
            new_items.append(item.dict())
        uniq_index_name = f'uniq{db_model.__name__}'
        stmt = insert(db_model).values(new_items).on_conflict_do_nothing(index_where=(uniq_index_name, ))
        await self.session.execute(stmt)
        await self.session.flush()
        await self.session.commit()

    async def add_launches(self, launches: List[Launch]):
        await self.insert_data(launches, LaunchTable)

    async def add_rockets(self, rockets: List[Rocket]):
        await self.insert_data(rockets, RocketTable)

    async def add_missions(self, missions: List[Mission]):
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
