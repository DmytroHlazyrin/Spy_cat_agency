from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.services.breed_validator import BreedValidator


# =========================================
# SpyCat schemas
# =========================================
class SpyCatBase(BaseModel):
    name: str = Field(
        ..., example="Shadow", description="The name of the spy cat"
    )
    years_of_experience: int = Field(
        ..., ge=0, example=3, description="Years of experience as a spy"
    )
    breed: str = Field(
        ..., example="Siamese", description="The breed of the spy cat"
    )
    salary: float = Field(
        ..., ge=0, example=1500.50, description="The cat's salary"
    )

    @field_validator("breed")
    @classmethod
    def validate_breed(cls, breed):
        if breed:
            BreedValidator.validate_breed(breed)
        return breed


class SpyCatCreate(SpyCatBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: Optional[float] = Field(
        None,
        ge=0,
        example=2000.00,
        description="Updated salary of the spy cat"
    )


class SpyCatResponse(SpyCatBase):
    id: int = Field(
        ..., example=1, description="The unique identifier of the spy cat"
    )

    model_config = ConfigDict(from_attributes=True)


# =========================================
# Target schemas
# =========================================

class TargetBase(BaseModel):
    name: str = Field(
        ...,
        example="Target Alpha",
        description="The name of the target"
    )
    country: str = Field(
        ...,
        example="Ukraine",
        description="The country where the target is located"
    )
    notes: Optional[str] = Field(
        None, example="Target spotted near the building",
        description="Notes about the target"
    )
    is_complete: bool = Field(
        False, description="Completion status of the target"
    )


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = Field(
        None, example="Updated note",
        description="Updated notes about the target"
    )
    is_complete: Optional[bool] = Field(
        None, description="Updated completion status of the target"
    )


class TargetResponse(TargetBase):
    id: int = Field(
        ..., example=1, description="The unique identifier of the target"
    )

    model_config = ConfigDict(from_attributes=True)


# =========================================
# Mission schemas
# =========================================

class MissionBase(BaseModel):
    is_complete: bool = Field(
        False, description="Completion status of the mission"
    )


class MissionUpdate(BaseModel):
    is_complete: Optional[bool] = Field(
        None, description="Updated completion status of the mission"
    )
    cat_id: Optional[int] = Field(
        None, description="Updated ID of the spy cat assigned to the mission"
    )
    targets: Optional[List[int]] = Field(
        None, description="Updated IDs of the targets assigned to the mission"
    )


class MissionCreate(MissionBase):
    targets: List[TargetCreate] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="A list of targets for the mission"
    )
    cat_id: Optional[int] = Field(
        None,
        description="The ID of the spy cat assigned to the mission"
    )


class MissionResponse(MissionBase):
    id: int = Field(
        ...,
        example=1,
        description="The unique identifier of the mission"
    )
    targets: List[TargetResponse] = Field(
        ...,
        description="A list of targets within the mission"
    )
    cat_id: Optional[int] = Field(
        None,
        description="The ID of the spy cat assigned to the mission"
    )

    model_config = ConfigDict(from_attributes=True)
