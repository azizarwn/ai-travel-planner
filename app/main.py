from fastapi import FastAPI
from app.modules.itinerary.router import itinerary_router

app = FastAPI(title="AI Travel Planner : Muslim Friendly")

app.include_router(itinerary_router)
