from fastapi import FastAPI
from app.routers import cats, targets, missions

app = FastAPI()

app.include_router(cats.router, tags=["Cats"])

app.include_router(targets.router, tags=["Targets"])

app.include_router(missions.router, tags=["Missions"])
