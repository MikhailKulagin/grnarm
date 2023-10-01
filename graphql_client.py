import datetime
from typing import List, Union

from base.httpx_client import AsyncBaseClient
from models import Launch, Mission, Rocket


class AsyncGraphQLClient(AsyncBaseClient):
    def __init__(self, host_cfg):
        super().__init__(host_cfg)

    @staticmethod
    def render(item: dict, data_model: Union[Launch, Mission, Rocket]) -> Union[Launch, Mission, Rocket]:
        res = data_model(**item)
        res.tstamp = datetime.datetime.now()
        return res

    async def get_data(self, body: str, data_name: str, data_model: Union[Launch, Mission, Rocket])\
            -> Union[List[Launch], List[Mission], List[Rocket]]:
        # TODO: Нужна человеческая пагинация через курсор
        params = {"limit": 100, "offset": 0}
        res = []
        while True:
            post_res = await self._post(url="", body={"query": body, "variables": params})
            if 'data' not in post_res:
                break
            data = post_res['data']
            if data_name not in data:
                break
            items = data[data_name]
            if not items:
                break
            res.extend([self.render(item, data_model) for item in items])
            params['limit'] = params['limit'] + 100
            params['offset'] = params['offset'] + 100
        return res

    async def get_launches_graph(self) -> List[Launch]:
        body = """
                query Launch($limit: Int, $offset: Int) {
                  launches(limit: $limit, offset: $offset) {
                    mission_name
                    launch_date_utc
                    details
                    is_tentative
                    launch_date_local
                    launch_date_unix
                    launch_success
                    launch_year
                    mission_name
                    static_fire_date_unix
                    static_fire_date_utc
                    tentative_max_precision
                    upcoming
                  }
                }
               """
        res = await self.get_data(body, data_name='launches', data_model=Launch)
        return res

    async def get_missions_graph(self) -> List[Mission]:
        body = """
                query Missions($limit: Int, $offset: Int) {
                  missions(limit: $limit, offset: $offset) {
                    name
                    description
                    manufacturers
                    twitter
                    website
                    wikipedia
                  }
                }
               """
        res = await self.get_data(body, data_name='missions', data_model=Mission)
        return res

    async def get_rockets_graph(self) -> List[Rocket]:
        body = """
                query Rockets($limit: Int, $offset: Int) {
                  rockets(limit: $limit, offset: $offset) {
                    name
                    description
                    active
                    boosters
                    company
                    cost_per_launch
                    country
                    first_flight
                    stages
                    success_rate_pct
                    type
                    wikipedia
                  }
                }
               """
        res = await self.get_data(body, data_name='rockets', data_model=Rocket)
        return res
