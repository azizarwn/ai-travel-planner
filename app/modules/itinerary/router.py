from app.modules.itinerary.schema import Itinerary
from app.modules.itinerary.prompt import SYSTEM_PROMPT
from app.utils.openai import client

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

itinerary_router = APIRouter(prefix="/itinerary", tags=["itinerary"])


@itinerary_router.get("/")
def get_itinerary(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@itinerary_router.post("/")
def create_itinerary(
    request: Request,
    destination: str = Form(...),
    days: int = Form(...),
    person: str = Form(...),
    interests: str = Form(...),
):
    user_input = (
        f"Destination: {destination}\n"
        f"Days of stay: {days}\n"
        f"Number of travelers: {person}\n"
        f"Preferences: {interests}"
    )

    res = client.chat.completions.parse(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        extra_body={"reasoning": {"enabled": True}},
        response_format=Itinerary,
    )

    itinerary: Itinerary = res.choices[0].message.parsed

    if itinerary is None:
        raise HTTPException(
            status_code=500, detail="Failed to parse itinerary response"
        )

    return templates.TemplateResponse(
        "result.html", {"request": request, "itinerary": itinerary}
    )
