from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER-API-KEY"), base_url="https://openrouter.ai/api/v1"
)
