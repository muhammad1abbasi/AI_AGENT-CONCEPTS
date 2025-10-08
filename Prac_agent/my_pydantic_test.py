from agents import Agent , Runner , OpenAIChatCompletionsModel , function_tool
import os 
from dotenv import load_dotenv
from agents import set_tracing_disabled
from openai import AsyncOpenAI
from typing import Literal , Optional
from my_pydantic_test import BaseModel

load_dotenv()

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)


class booking_responce (BaseModel):
    status: Literal["success", "failure"]
    booking_id: Optional[str]
    message = str



booking_agent = Agent(
    name="booking_expert",
    instructions="You are a booking agent. Always reply using BookingResponse schema",
    model=model,
    output_type=booking_responce
)


result = Runner.run(booking_agent, input="Book 2 tikcetes for towmorrow")
print(result.final_ouput)