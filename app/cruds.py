from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from .models import SpyCat, Mission, Target
from .schemas import SpyCatCreate, SpyCatUpdate, MissionCreate, TargetUpdate, \
    MissionUpdate, TargetCreate
from .services.breed_validator import BreedValidator


# CRUD for SpyCat
async def create_spycat(cat: SpyCatCreate, session: AsyncSession) -> SpyCat:
    """Create a new spy cat."""
    try:
        BreedValidator.validate_breed(cat.breed)
        new_cat = SpyCat(**cat.dict())
        session.add(new_cat)
        await session.commit()
        await session.refresh(new_cat)
        return new_cat
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to create spy cat due to integrity error."
        )


async def get_spycat(cat_id: int, session: AsyncSession) -> SpyCat:
    """Retrieve a single spy cat by ID."""
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    spycat = result.scalar_one_or_none()
    if not spycat:
        raise HTTPException(status_code=404, detail="Spy cat not found.")
    return spycat


async def list_spycats(session: AsyncSession) -> List[SpyCat]:
    """Retrieve all spy cats."""
    result = await session.execute(select(SpyCat))
    return result.scalars().all()


async def update_spycat(
        cat_id: int,
        update_data: SpyCatUpdate,
        session: AsyncSession
) -> SpyCat:
    """Update salary for a specific spy cat."""
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    spycat = result.scalar_one_or_none()
    if not spycat:
        raise HTTPException(status_code=404, detail="Spy cat not found.")
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(spycat, field, value)
    await session.commit()
    await session.refresh(spycat)
    return spycat


async def delete_spycat(cat_id: int, session: AsyncSession) -> dict:
    """Delete a spy cat."""
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    spycat = result.scalar_one_or_none()
    if not spycat:
        raise HTTPException(status_code=404, detail="Spy cat not found.")
    await session.delete(spycat)
    await session.commit()
    return {"detail": "Spy cat deleted successfully."}


# CRUD for Mission
async def create_mission(
        mission: MissionCreate,
        session: AsyncSession
) -> Mission:
    """Create a new mission with targets."""
    # Create the mission object first
    new_mission = Mission(is_complete=mission.is_complete)

    # If there is a cat assigned, associate it with the mission
    if mission.cat_id:
        result = await session.execute(
            select(SpyCat).where(SpyCat.id == mission.cat_id)
        )
        spycat = result.scalar_one_or_none()
        if not spycat:
            raise HTTPException(status_code=404, detail="Spy cat not found.")
        new_mission.cat_id = mission.cat_id

    session.add(new_mission)

    # Flush to generate a mission ID before associating targets
    await session.flush()

    # Now create and associate the targets
    targets = [Target(
        **target.dict(),
        mission_id=new_mission.id
    ) for target in mission.targets]
    session.add_all(targets)

    # Commit all changes
    await session.commit()

    # Refresh mission and targets data
    await session.refresh(new_mission)

    # Reload mission to include loaded targets
    result = await session.execute(
        select(Mission).where(Mission.id == new_mission.id).options(
            selectinload(Mission.targets))
    )
    new_mission = result.scalar_one_or_none()

    return new_mission


async def get_mission(mission_id: int, session: AsyncSession) -> Mission:
    """Retrieve a specific mission by ID, including related targets."""
    result = await session.execute(
        select(Mission)
        .where(Mission.id == mission_id)
        .options(selectinload(Mission.targets))
        # Ensure related targets are loaded
    )
    mission = result.scalar_one_or_none()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found.")

    return mission


async def list_missions(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> List[Mission]:
    """Retrieve all missions, including their related targets."""
    result = await session.execute(
        select(Mission)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Mission.targets))
        # Ensure related targets are loaded
    )
    missions = result.scalars().all()

    if not missions:
        raise HTTPException(status_code=404, detail="No missions found.")

    return missions


async def mark_mission_as_completed(
        mission_id: int,
        session: AsyncSession
) -> Mission:
    """Update a mission, including its targets."""
    # Retrieve the mission by ID
    result = await session.execute(
        select(Mission).where(Mission.id == mission_id).options(
            selectinload(Mission.targets))
    )
    mission = result.scalar_one_or_none()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found.")

    mission.is_complete = True

    await session.commit()
    await session.refresh(mission)
    return mission


async def assign_cat_to_mission(
        mission_id: int,
        cat_id: int, session: AsyncSession
) -> Mission:
    """Assign a cat to a mission."""
    # Retrieve the mission by ID
    result = await session.execute(
        select(Mission).where(Mission.id == mission_id).options(
            selectinload(Mission.targets))
    )
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found.")

    # Retrieve the cat by ID
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found.")

    mission.cat_id = cat_id

    await session.commit()
    await session.refresh(mission)
    return mission


async def update_mission(
        mission_id: int,
        update_data: MissionUpdate,
        session: AsyncSession
) -> Mission:
    """Update mission details, including its targets."""
    result = await session.execute(
        select(Mission).where(Mission.id == mission_id).options(
            selectinload(Mission.targets))
    )
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found.")
    if mission.cat_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot update a mission assigned to a cat."
        )
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(mission, field, value)
    await session.commit()
    await session.refresh(mission)
    return mission


async def delete_mission(mission_id: int, session: AsyncSession) -> dict:
    """Delete a mission if it is not assigned to a cat."""
    result = await session.execute(
        select(Mission).where(Mission.id == mission_id)
    )
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(
            status_code=404,
            detail="Mission not found."
        )
    if mission.cat_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a mission assigned to a cat."
        )
    await session.delete(mission)
    await session.commit()
    return {"detail": "Mission deleted successfully."}


async def add_target_to_mission(
        mission_id: int,
        target_data: TargetCreate,
        session: AsyncSession
) -> Target:
    """Add a target to a mission."""
    result = await session.execute(
        select(Mission).where(Mission.id == mission_id).options(
            selectinload(Mission.targets))
    )
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(
            status_code=404,
            detail="Mission not found."
        )
    if mission.is_complete:
        raise HTTPException(
            status_code=400,
            detail="Targets for a completed mission cannot be added."
        )
    if len(mission.targets) >= 3:
        raise HTTPException(
            status_code=400,
            detail="Maximum number of targets reached for a mission."
        )
    target = Target(**target_data.dict(), mission_id=mission_id)
    session.add(target)
    await session.commit()
    await session.refresh(target)
    return target


# CRUD for Target
async def update_target(
        target_id: int,
        update_data: TargetUpdate,
        session: AsyncSession
) -> Target:
    """Update target notes or completion status."""
    result = await session.execute(
        select(Target).where(Target.id == target_id).options(
            selectinload(Target.mission))
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found.")
    if target.is_complete:
        raise HTTPException(
            status_code=400,
            detail="Completed targets cannot be updated."
        )
    mission = target.mission
    if mission and mission.is_complete:
        raise HTTPException(
            status_code=400,
            detail="Targets for a completed mission cannot be updated."
        )
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(target, field, value)
    await session.commit()
    await session.refresh(target)
    return target
