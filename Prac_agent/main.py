from agents import Agent , Runner , OpenAIChatCompletionsModel , function_tool
import os 
from dotenv import load_dotenv
from agents import set_tracing_disabled
from openai import AsyncOpenAI

load_dotenv()

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

@function_tool
def add(a:int , b: int): 
    print("add called")
    return a + b 

@function_tool
def subtraction(a: int , b: int):
    print("subtraction called")
    return a - b 

agent = Agent(
    name="Maths_Agent",
    instructions="""
You are a helful math agent if youser ask for addition then call add tool function
if user asks for subtraction then call subtraction function
""",
    model=model,
    tools=[add , subtraction],
)


print(Runner.run_sync(agent , input="what is sum of 6 and 8"))
print(Runner.run_sync(agent , input="what is sub of 6 and 2"))