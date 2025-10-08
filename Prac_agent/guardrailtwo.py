from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    set_tracing_disabled, input_guardrail,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered
)
from my_pydantic_test import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Define output type for guardrail
class MathHomeworkCheck(BaseModel):
    is_math_homework: bool
    reasoning: str

# Guardrail agent (checks if input is math homework)
guardrail_agent = Agent(
    name="Math Homework Check Agent",
    instructions="Check if the user is asking to do their math homework.",
    model=model,
    output_type=MathHomeworkCheck
)

# Input guardrail function
@input_guardrail
async def math_guardrail(ctx, agent, input_str: str) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input_str, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework
    )

# Main agent
agent = Agent(
    name="Customer Support Agent",
    instructions="Help customers with questions.",
    model=model,
    input_guardrails=[math_guardrail]
)

# Run
async def main():
    try:
        result = await Runner.run(agent, "Can you solve this equation 2x + 3 = 11?")
        print("Agent output:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Guardrail tripped: Math homework not allowed!")

    try:
        result = await Runner.run(agent, "How can I reset my account password?")
        print("✅ Agent output:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Guardrail tripped!")

if __name__ == "__main__":
    asyncio.run(main())


