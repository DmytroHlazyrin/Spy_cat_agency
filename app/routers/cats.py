from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import create_spycat, get_spycat, list_spycats, update_spycat, \
    delete_spycat
from app.database import get_async_session
from app.schemas import SpyCatResponse, SpyCatCreate, SpyCatUpdate

router = APIRouter()


# Routes for SpyCat
@router.post("/spycat/", response_model=SpyCatResponse, status_code=201)
async def create_spycat_route(
        cat: SpyCatCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await create_spycat(cat, session)


@router.get("/spycat/{cat_id}", response_model=SpyCatResponse)
async def get_spycat_route(
        cat_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_spycat(cat_id, session)


@router.get("/spycat/", response_model=List[SpyCatResponse])
async def list_spycats_route(
        session: AsyncSession = Depends(get_async_session)
):
    return await list_spycats(session)


@router.put("/spycat/{cat_id}", response_model=SpyCatResponse)
async def update_spycat_route(
        cat_id: int,
        update_data: SpyCatUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    return await update_spycat(cat_id, update_data, session)


@router.delete("/spycat/{cat_id}", status_code=204)
async def delete_spycat_route(
        cat_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await delete_spycat(cat_id, session)
