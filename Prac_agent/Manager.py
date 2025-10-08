from agents import Runner, OpenAIChatCompletionsModel, set_tracing_disabled , function_tool
from openai import AsyncOpenAI
from typing import Any
from dataclasses import dataclass
import os
import asyncio
from dotenv import load_dotenv
from agents import Agent
# Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# OpenAI-compatible Gemini client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model definition
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# # Sub-agents
# booking_agent = Agent(
#     name="booking_expert",
#     instructions="You are an expert booking assistant. Return short JSON: {status, booking_id, message}.",
#     model=model,
# )

# refund_agent = Agent(
#     name="refund_expert",
#     instructions="You are an expert on refunds. Return short JSON: {status, amount, message}.",
#     model=model,
# )

# # Tools
# booking_tool = booking_agent.as_tool(
#     tool_name="booking_expert",
#     tool_description="Handles booking questions and booking requests.",
# )

# refund_tool = refund_agent.as_tool(
#     tool_name="refund_expert",
#     tool_description="Handles refund questions and requests.",
# )

# # Manager agent
# manager_instructions = (
#     "You are the customer-facing agent. Engage with the user naturally. "
#     "If the query is about booking, call the booking_expert tool. "
#     "If the query is about refunds, call the refund_expert tool. "
#     "Summarize the tool’s JSON output into a clear, human-readable final response."
# )

# manager_agent = Agent(
#     name="customer_facing_agent",
#     instructions=manager_instructions,
#     model=model,
#     tools=[booking_tool, refund_tool],
# )

# # Runner instance
# runner = Runner()

# # User context (dataclass example)
# @dataclass
# class UserContext:
#     user_id: str
#     user_name: str

# # Main async function
# async def main():
#     ctx = UserContext(user_id="u123", user_name="Zulfi Khito")
#     result = await runner.run(
#         starting_agent=manager_agent,
#         input="I want to book a ticket for tomorrow evening for two people.",
#         context=ctx,
#     )
#     print("\n=== Final Result ===")
#     print(result.output)
#     print("====================\n")

# # Correct entry point
# if __name__ == "__main__":
#     asyncio.run(main())

# pirate_agent = Agent(
#     name="Pirate",
#     instructions="Write like a pirate",
#     model="o3-mini",
# )

# robot_agent = pirate_agent.clone(
#    name="The agent",
#    instructions="bluh",
#    t
# )


# @function_tool
# def weather(city: str)-> str:
#     print("weather tool called")
#     return('the weather of', {city} , "is 45c")
# @function_tool
# def math(num1 , num2):
#     print("math tool called")
#     return num1 + num2

# agent = Agent(
#     name="weather agent",
#     instructions="Your are a problem solver agent if user ask for weather then use weather tool and if user ask for calculation then use math tool and if ask for both give both answers",
#     model=model,
#     tools=[math, weather],
#     tool_use_behavior="stop_on_first_tool"
# )

# result = Runner.run_sync(
#     agent , input="""
# Tell what is the sum of 2 and 9 and weather of islamabad 
# """
# )

# print(result.final_output)


# agentone = Agent (
#     name="agentone",
#     instructions="bluh bluh",
#     model=model
# )

# agenttwo = Agent(
#     name="agenttwo",
#     instructions="bluh",
#     model=model
# )

# agentonetool = agentone.as_tool(
#     tool_name="hasim",
#     tool_description="fsfsdf"
#     )


# agenttwotool = agenttwo.as_tool(
#     tool_name="hello",
#     tool_description="what every"
# )

# @function_tool
# def addintion(num1 , num2):
#     return num1 + num2


# dynamic_ins = """hello please use both of them tools as agents"""


# main_agent = Agent(
#     name="manager",
#     instructions=dynamic_ins,
#     model=model,
#     tools=[agentonetool, agenttwotool, addintion]
# )


# result = Runner.run(main_agent , input="Hello what you can do for me ")
# print(result.final_output)