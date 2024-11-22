import requests
from fastapi import HTTPException
from apscheduler.schedulers.background import BackgroundScheduler


class BreedValidator:
    _cached_breeds = None  # Cache for cached breeds
    _api_url = "https://api.thecatapi.com/v1/breeds"

    @classmethod
    def fetch_breeds(cls):
        """Request breeds from TheCatAPI and update the cache"""
        try:
            response = requests.get(cls._api_url)
            response.raise_for_status()
            breeds = [breed["name"] for breed in response.json()]
            cls._cached_breeds = breeds
        except requests.RequestException:
            raise HTTPException(
                status_code=503, detail="Could not connect to TheCatAPI."
            )

    @classmethod
    def is_valid_breed(cls, breed: str) -> bool:
        """Check if the bread is valid"""
        if cls._cached_breeds is None:
            cls.fetch_breeds()
        return breed in cls._cached_breeds

    @classmethod
    def validate_breed(cls, breed: str):
        """Raise an HTTPException if the breed is not valid"""
        if not cls.is_valid_breed(breed):
            raise HTTPException(
                status_code=400, detail=f"Breed '{breed}' not found."
            )


def update_breeds_cache():
    BreedValidator.fetch_breeds()


scheduler = BackgroundScheduler()
scheduler.add_job(update_breeds_cache, "interval", hours=6)
scheduler.start()
