from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import update_target
from app.database import get_async_session
from app.schemas import TargetResponse, TargetUpdate

router = APIRouter()


# Routes for Target
@router.put("/target/{target_id}", response_model=TargetResponse)
async def update_target_route(
        target_id: int,
        update_data: TargetUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> TargetResponse:
    """Update a target by ID."""
    return await update_target(target_id, update_data, session)
