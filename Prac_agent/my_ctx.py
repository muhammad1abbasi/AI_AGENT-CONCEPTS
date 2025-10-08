from agents import (Agent,
                    OpenAIChatCompletionsModel,
                    Runner,
                    function_tool,
                    handoff,
                    set_tracing_disabled,
                    RunContextWrapper,
                    model_settings,
                    )
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import os
from dataclasses import dataclass

load_dotenv()
set_tracing_disabled(disabled=True)

client =AsyncOpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=client
)


@dataclass
class userinfo:
    uid: int
    name: str


@function_tool
def fetch_your_age(wrapper: RunContextWrapper[userinfo]):
    return f"The user {wrapper.context.name} is 24 years old"


async def main():
    user_info = userinfo(uid=3 , name="Muhmmad")

    agent = Agent[userinfo](
        name="my_agent",
        instructions="""
    If the user asks about age, you MUST always call the tool fetch_your_age 
    instead of answering directly.
    """,
        tools=[fetch_your_age],
        model=model,
        # tool_use_behavior="stop_on_first_tool",
        # model_settings=model_settings(tool_choice="required")
    )

    result = await Runner.run(agent, input='what is the age of user?', context=user_info)
    print(result.final_output)


asyncio.run(main())