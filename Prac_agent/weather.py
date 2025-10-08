from agents import  (Runner ,
                      OpenAIChatCompletionsModel ,
                        AgentHooks ,
                          function_tool ,
                            set_tracing_disabled ,
                            )
import  os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from agents import Agent
import asyncio
load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_tracing_disabled(disabled=True)


model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# @function_tool
# def get_weather(city: str):
#     print("get_weather_tool_called")

#     if city.lower() == "lahore":
#         return "the weater in lahore is 30C and sunny"
#     elif city.lower() == "islamabad":
#         return("the weather in islamabad is 25C and cloudy")
#     else:
#         return f"sorry i dont have weather info except lahore and islamabad"
    

# class AgentHooks(AgentHooks):
#     async def on_start(self , context , agent):
#         print(f"[AgentHook] Agent '{agent.name}' is starting")

#     async def on_tool_call(self , context , agent , tool):
#         print(f"[AgentHooks] Agcent '{agent.name}' tool called {tool.name} ")

#     async def on_loo_end(self , context , agent , tool, result):
#         print(f"[AgentHooks] Agent '{agent.name}' {tool.name} end with result {result}")

#     async def on_end(self , context , agent , output):
#         print(f"[AgentHooks] Agent '{agent.name}' finish with output '{output}'")
        


# agent = Agent(
#     name="weater_agent",
#     instructions="You are a helpful weather agent. if user asks for weather condithion then tell him and you have only lahore and islam abad weather condition dont give other countries city weather",
#     model=model,
#     tools=[get_weather],
#     hooks=AgentHooks()
# )

# async def main():
#     result = await Runner.run(agent , input="what is weather condition in lahore and islamabad and  karachi")
#     print("final output", result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())



@function_tool
def Weather(city: str):
    print("Weather tool excecuted")
    if city.lower() == "lahore":
        return("The weather of lahore is 35`C")
    elif city.lower() == "karachi":
        return("The weather of karachi is 77`c")
    else:
        return("Iam really sorry i dont have this city information try again")

class Hooks(AgentHooks):
    async def on_start(self , context , agent):
        print(f"[AgentHooks] Agent '{agent.name}' Is running")

    async def on_tool_start(self , context , agent ,  tool ):
        print(f"[AgentHooks] Agent '{agent.name}' running tool '{tool.name}'")

    async def on_tool_end(self , context , tool , agent ,  result):
        print(f"[AgentHooks] Agent , '{agent.name} , result '{result}''")

    async def on_end(self , context , agent , output):
        print(f"[AgentHooks] Agent '{agent.name}' final output '{output}'")


agent  = Agent(
    name="Weather agent",
    instructions="You are a weather agent if user ask for karachi weather codition and call Weahtertwo tool for give information",
    model=model,
    tools=[Weather],
    hooks= Hooks()
)

async def main():
    result = await Runner.run(agent , input="what is weather condition Karachi and lahore ")
    print("final output", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
