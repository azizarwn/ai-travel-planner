from pydantic import BaseModel, Field


class Activity(BaseModel):
    name: str = Field(description="name of the activity")
    description: str = Field(description="description of the activity")
    location: str = Field(description="location of the activity")


class ItineraryDay(BaseModel):
    day_number: int = Field(description="day number in the itinerary")
    activities: list[Activity] = Field(description="list of activities for the day")
    attractions: list[str] = Field(description="list of attractions for the day")
    dining_options: list[str] = Field(description="list of dining place for the day")
    estimated_budget: int = Field(description="estimated budget for the day in USD")


class Itinerary(BaseModel):
    destination: str = Field(description="destination of the itinerary")
    days_of_stay: int = Field(description="number of days in the itinerary")
    total_person: str = Field(description="total person in the itinerary")
    preferences: str = Field(description="preferences of the traveler")
    itinerary: list[ItineraryDay] = Field(description="list of itinerary day")
