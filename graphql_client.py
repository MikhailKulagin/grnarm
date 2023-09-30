from typing import List, Union

from base.httpx_client import AsyncBaseClient
from models import Launch, Mission, Rocket


class AsyncGraphQLClient(AsyncBaseClient):
    def __init__(self, host_cfg):
        super().__init__(host_cfg)

    async def get_data(self, body: str, data_name: str, data_model: Union[Launch, Mission, Rocket])\
            -> Union[List[Launch], List[Mission], List[Rocket]]:
        params = {"limit": 100, "offset": 0}
        res = []
        while True:
            post_res = self._post(url="", body={"query": body, "variables": params})
            if 'data' not in post_res:
                break
            data = post_res['data']
            if data_name not in data:
                break
            items = data[data_name]
            if not items:
                break
            res.extend([data_model(**item) for item in items])
            params['limit'] = params['limit'] + 100
            params['offset'] = params['offset'] + 100
        return res

    async def get_data_pagination(self):
        pass

    async def get_launches_graph(self) -> List[Launch]:
        body = """
                query Launch($limit: Int, $offset: Int) {
                  launches(limit: $limit, offset: $offset) {
                    mission_name
                    launch_date_utc
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
                  }
                }
               """
        res = await self.get_data(body, data_name='rockets', data_model=Rocket)
        return res
