from agents import Agent , Runner , OpenAIChatCompletionsModel , function_tool, set_tracing_disabled
import os 
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# -------- STATE --------
todo_list = []

# -------- TOOLS --------
@function_tool
def add_todo(task: str):
    todo_list.append(task)
    return f"Task '{task}' added to your todo list."

@function_tool
def remove_task(task: str):
    if task in todo_list:
        todo_list.remove(task)
        return f"Task '{task}' removed successfully."
    else:
        return "Task not found."

@function_tool
def show_task():
    if not todo_list:
        return "Todo list is empty."
    return "Your tasks: " + ", ".join(todo_list)

# -------- AGENT --------
agent = Agent(
    name="Todo list Agent",
    instructions="You help manage a to-do list. Use tools to add, remove, or show tasks.",
    tools=[add_todo , remove_task , show_task],
    model=model
)

# -------- MAIN --------
async def main():
    print("👉 Try commands like: 'Add buy milk', 'Remove buy milk', 'Show my tasks'")

    result1 = await Runner.run(agent , input="Add buy milk")
    print("Result 1:", result1.final_output)

    result2 = await Runner.run(agent, input="Add go gym")
    print("Result 2:", result2.final_output)

    result3 = await Runner.run(agent, input="Show my tasks")
    print("Result 3:", result3.final_output)

    result4 = await Runner.run(agent, input="Remove buy milk")
    print("Result 4:", result4.final_output)

    result5 = await Runner.run(agent, input="Show my tasks")
    print("Result 5:", result5.final_output)

    result6 = await Runner.run(agent , input="show me all saved tasks one by one ")
    print("Result 6:", result6.final_output)
if __name__ == "__main__":
    asyncio.run(main())
