import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import config
from graphql_client import AsyncGraphQLClient
from database.process import DbClient
from database.db import get_session

router = APIRouter()
log = logging.getLogger(__name__)

api_client = AsyncGraphQLClient(config.graphql)


@router.get("/get_launches")
async def get_launches(session: Session = Depends(get_session)):
    """
    Полуачем данные launches
    """
    graph_res = await api_client.get_launches_graph()
    print(graph_res)
    db_client = DbClient(session)
    await db_client.add_launches(graph_res)


@router.get("/get_missions")
async def get_missions(session: Session = Depends(get_session)):
    """
    Полуачем данные missions
    """
    graph_res = await api_client.get_missions_graph()
    print(graph_res)
    db_client = DbClient(session)
    await db_client.add_missions(graph_res)


@router.get("/get_rockets")
async def get_rockets(session: Session = Depends(get_session)):
    """
    Полуачем данные rockets
    """
    graph_res = await api_client.get_rockets_graph()
    print(graph_res)
    db_client = DbClient(session)
    await db_client.add_rockets(graph_res)


@router.get("/get_totals")
async def get_rockets(session: Session = Depends(get_session)):
    """
    Считаем тоталы по всем таблицам, которые описаны в классах db_models.
    (t_missions, t_launches, t_rockets)
    :param session:
    :return:
    """
    db_client = DbClient(session)
    res = await db_client.select_totals()
    print(res)
