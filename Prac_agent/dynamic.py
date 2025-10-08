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
class user_info:
    name: str
    is_premium: bool


def dynamic_ins(context: RunContextWrapper[user_info], agent = Agent[user_info])-> str:
    user=context.context
    if user.is_premium:
        return f"{user.name} You are a premium user. Assist with priority and provide detailed answers."
    else:
        return f"{user.name}  You are a free user. Keep answers short and polite"
    
agent = Agent(
    name="Personal chat agent",
    instructions=dynamic_ins,
    model=model
)

async def main():
    ctx1 = user_info(name="Muhammad", is_premium=True)
    result1 = await Runner.run(agent , input="Explain quantum computing" , context=ctx1)
    print(result1.final_output)

    
    ctx2 = user_info(name="daniyal" , is_premium=False)
    result2 = await Runner.run(agent , input="Explain quantum computing", context=ctx2)

    print(result2.final_output)


if __name__ == '__main__':
    asyncio.run(main())