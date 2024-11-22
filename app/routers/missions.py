from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import create_mission, get_mission, list_missions, \
    mark_mission_as_completed, delete_mission, update_mission, \
    assign_cat_to_mission, add_target_to_mission
from app.database import get_async_session
from app.schemas import MissionResponse, MissionCreate, MissionUpdate, \
    TargetCreate, TargetResponse

router = APIRouter()


# Routes for Mission
@router.post("/mission/", response_model=MissionResponse)
async def create_mission_route(
        mission: MissionCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await create_mission(mission, session)


@router.get("/mission/{mission_id}", response_model=MissionResponse)
async def get_mission_route(
        mission_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_mission(mission_id, session)


@router.get("/mission/", response_model=List[MissionResponse])
async def list_missions_route(
        session: AsyncSession = Depends(get_async_session)
):
    return await list_missions(session)


@router.post(
    "/mission/{mission_id}/assign_cat",
    response_model=MissionResponse
)
async def assign_cat_to_mission_route(
        mission_id: int,
        cat_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await assign_cat_to_mission(mission_id, cat_id, session)


@router.post(
    "/mission/{mission_id}/mark_as_completed",
    response_model=MissionResponse
)
async def update_mission_route(
        mission_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await mark_mission_as_completed(mission_id, session)


@router.post("/mission/{mission_id}/add_target", response_model=TargetResponse)
async def add_target_to_mission_route(
        mission_id: int,
        target_data: TargetCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await add_target_to_mission(mission_id, target_data, session)


@router.delete("/mission/{mission_id}")
async def delete_mission_route(
        mission_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await delete_mission(mission_id, session)
