from agents import  Runner , OpenAIChatCompletionsModel , AgentHooks , function_tool , set_tracing_disabled
import  os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from agents import Agent
load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_tracing_disabled(disabled=True)


model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)


@function_tool
def greetings_tool(name: str): 
    print("greetings called")
    return f"Hello {name}"


class AgentHooks(AgentHooks):
    async def on_start(self , context , agent):
        print(f"[AgentHooks] Agent '{agent.name}' is starting")

    async def on_tool_call(self , context , agent , tool):
        print(f"[AgentHooks] Agent '{agent.name}' is calling tool '{tool.name}'")

    async def on_tool_end(self , context , agent , tool, result):
        print(f"[AgentHooks] Agent '{agent.name}' returned: '{result}'")

    async def on_end(self , context , agent , output):
        print(f"[AgentHooks] Agent '{agent.name}' finish with output '{output}'")

agent = Agent(
    name="Greeting_Agent",
    instructions="Say hello when asked to greet someone.",
    model=model,
    tools=[greetings_tool],
    hooks=AgentHooks()
)

async def main():
    result = await Runner.run(agent , input="greet david corensweth superman")
    print("final output", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())