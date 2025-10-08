# from agents import (Agent,
#                     OpenAIChatCompletionsModel,
#                     Runner,
#                     function_tool,
#                     handoff,
#                     set_tracing_disabled
#                     )
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# import asyncio
# import os

# load_dotenv()
# set_tracing_disabled(disabled=True)

# client =AsyncOpenAI(
#     api_key = os.getenv("GEMINI_API_KEY"),
#     base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model='gemini-2.0-flash',
#     openai_client=client
# )

# math_teacher = Agent(
#     name="math teacher",
#     instructions="if user ask for math related questions then answer them Always prefix your answer with [Math Teacher]:",
#     model=model,
# )

# it_teacher = Agent(
#     name="it_expert_agent",
#     instructions="You are an expert IT teacher. "
#         "If a user asks about computers, programming, networking, or IT concepts, "
#         "you must always answer clearly and confidently. "
#         "Always prefix your reply with: [IT Expert]:",
#     model=model
# )

# agent = Agent(
#     name="main agent",
#     instructions="""
# You are main agent you work is when user ask for math related questions so handoff that task to math agent
# and if user ask for IT related question then handoff to task it_expert_agent and then give answers
# """,
# handoffs=[math_teacher, it_teacher],
# model= model

# )

# result =  asyncio.run(Runner.run(agent , input="""
# "Please give me answer of wht is some of 2 + 2
# """))

# result2 = asyncio.run(Runner.run(agent , input="What is Python used for?"))
# print(result.final_output)
# print(result2.final_output)

print("Hello world")