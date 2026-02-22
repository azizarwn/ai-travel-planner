from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER-API-KEY"), base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
You are a helpful travel assistant that creates detailed itineraries for travelers, especially for Muslim travelers.
When given a destination and duration, you will generate a day-by-day itinerary that includes recommended activities,
attractions, dining options, and any necessary travel information.
Your responses should be informative, engaging, and tailored to the user's preferences if provided.
<example_output>
itinerary for {how many days} days in {destination}:
# Day {day number}: 
- Activities: {list of activities}
- Attractions: {list of attractions}
- Dining Options: {list of dining options}
- Travel Information: {any necessary travel information for the day}
</example_output>

<guidelines>
 - Detail for day 1 are about departure from origin city.
 - make sure all destination area reached in same day and is close to each other.
 - if need to move to another area, make sure to include travel information and time needed for the move.
 - include recommended activities, attractions, dining options, and any necessary travel information for each day.
 - make it friendly for muslim traveler, include halal dining options and prayer facilities if available.
 - on the last day, include details for return trip to origin city.
</guidelines>

<guardrails>
- Do not include any activities or dining options that are not suitable for Muslim travelers.
- Ensure that all travel information is accurate and up-to-date.
- Avoid recommending activities or attractions that are too far apart to be visited in the same day.
</guardrails>
"""

# res = client.chat.completions.create(
#     model="google/gemini-2.5-flash-lite",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {
#             "role": "user",
#             "content": "Create itinerary for 6 days in Kuala Lumpur, Malaysia and departed from Batam, Indonesia.",
#         },
#     ],
#     extra_body={"reasoning": {"enabled": True}},
# )

# result = res.choices[0].message.content


# class Sentiment(BaseModel):
#     sentiment: str = Field(
#         description="sentiment can be positive, negative, or neutral"
#     )
#     confidence_score: int = Field(description="minimum is 0, maximum is 10")


# res = client.chat.completions.parse(
#     model="google/gemini-2.5-flash-lite",
#     messages=[
#         {"role": "system", "content": "Extract the sentiment from user input"},
#         {
#             "role": "user",
#             "content": "The service and food at Ara Restaurant was so bad.",
#         },
#     ],
#     extra_body={"reasoning": {"enabled": True}},
#     response_format=Sentiment,
# )


# result = res.choices[0].message.parsed


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


user_input = """
    Destination: Seoul, South Korea
    Days of stay: 3 days
    Total person: 2 adults
    Preferences: Interested in cultural experiences, shopping, and trying local cuisine. Prefer halal dining options, give restaurant recommendation.
"""

res = client.chat.completions.parse(
    model="google/gemini-2.5-flash-lite",
    messages=[
        {
            "role": "system",
            "content": "Create an itinerary based on user context for day to day",
        },
        {
            "role": "user",
            "content": user_input,
        },
    ],
    extra_body={"reasoning": {"enabled": True}},
    response_format=Itinerary,
)


result = res.choices[0].message.parsed
print(result)
