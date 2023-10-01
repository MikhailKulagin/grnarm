import logging

from fastapi import APIRouter, Depends
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
    try:
        graph_res = await api_client.get_launches_graph()
        db_client = DbClient(session)
        res = await db_client.add_launches(graph_res)
        return res.dict()
    except Exception as err:
        logging.error(f'{err}')
        return {"error": err, "error_type": type(err).__name__, "error_details": err.args}


@router.get("/get_missions")
async def get_missions(session: Session = Depends(get_session)):
    """
    Полуачем данные missions
    """
    try:
        graph_res = await api_client.get_missions_graph()
        db_client = DbClient(session)
        res = await db_client.add_missions(graph_res)
        return {"add_data": res}
    except Exception as err:
        logging.error(f'{err}')
        return {"error": err, "error_type": type(err).__name__, "error_details": err.args}


@router.get("/get_rockets")
async def get_rockets(session: Session = Depends(get_session)):
    """
    Полуачем данные rockets
    """
    try:
        graph_res = await api_client.get_rockets_graph()
        db_client = DbClient(session)
        res = await db_client.add_rockets(graph_res)
        return {"add_data": res}
    except Exception as err:
        logging.error(f'{err}')
        return {"error": err, "error_type": type(err).__name__, "error_details": err.args}


@router.get("/get_totals")
async def get_rockets(session: Session = Depends(get_session)):
    """
    Считаем тоталы по всем таблицам, которые описаны в классах db_models.
    (t_missions, t_launches, t_rockets)
    :param session:
    :return:
    """
    try:
        db_client = DbClient(session)
        res = await db_client.select_totals()
        logging.info(f'current totals {res}')
        return res
    except Exception as err:
        logging.error(f'{err}')
        return {"error": err, "error_type": type(err).__name__, "error_details": err.args}


@router.get("/clear_all_data")
async def clear_all_data(session: Session = Depends(get_session)):
    """
    Чистим таблицы
    :param session:
    :return:
    """
    try:
        db_client = DbClient(session)
        return await db_client.clear_all_tables()
    except Exception as err:
        logging.error(f'{err}')
        return {"error": err, "error_type": type(err).__name__, "error_details": err.args}
