import logging
import datetime
from typing import List, Union
import sys, inspect
from sqlalchemy.future import select
from sqlalchemy.dialects.sqlite import insert

from models import Mission, Rocket, Launch, DefaultResponse, TotalResponse
from database.db_models import LaunchTable, MissionTable, RocketTable

log = logging.getLogger(__name__)


class DbClient:
    def __init__(self,
                 session
                 ):
        self.session = session

    async def insert_data(self,
                          data: Union[List[Mission], List[Launch], List[Rocket]],
                          db_model: Union[MissionTable, LaunchTable, RocketTable]):
        new_items = []
        # TODO: Убрать костыль. Graph возвращает строку с датой, которую не получается инсертить
        for item in data:
            for name, value in item.dict().items():
                if type(value) == datetime.datetime:
                    setattr(item, name, getattr(item, name).replace(tzinfo=None))
            new_items.append(item.dict())
        uniq_index_name = f'uniq{db_model.__name__}'
        if new_items:
            stmt = insert(db_model).values(new_items).on_conflict_do_nothing(index_where=(uniq_index_name, ))
            res = await self.session.execute(stmt)
            await self.session.flush()
            await self.session.commit()
            if res.rowcount:
                logging.info('insert new data')
                return True
        logging.info('no new data')
        return False

    async def add_launches(self, launches: List[Launch]):
        res = await self.insert_data(launches, LaunchTable)
        return DefaultResponse(**{"result": res})

    async def add_rockets(self, rockets: List[Rocket]):
        res = await self.insert_data(rockets, RocketTable)
        return DefaultResponse(**{"result": res})

    async def add_missions(self, missions: List[Mission]):
        res = await self.insert_data(missions, MissionTable)
        return DefaultResponse(**{"result": res})

    async def select_totals(self):
        count_res = {}
        for t_name, obj in inspect.getmembers(sys.modules["database.db_models"]):
            if t_name.endswith("Table"):
                q = select(obj.id)
                res = await self.session.execute(q)
                curr = res.scalars()
                count = len([_ for _ in curr])
                count_res[t_name] = count
        return TotalResponse(**count_res)

    async def clear_all_tables(self):
        await self.session.execute("""truncate table public.t_launches""")
        await self.session.execute("""truncate table public.t_missions""")
        await self.session.execute("""truncate table public.t_rockets""")
        await self.session.commit()
        logging.info('clear all tables')
        return DefaultResponse(**{"result": True})
