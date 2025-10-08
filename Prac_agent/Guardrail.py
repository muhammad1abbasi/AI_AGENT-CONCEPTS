import asyncio
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    input_guardrail,
    GuardrailFunctionOutput,
    set_tracing_disabled,
)
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from my_pydantic_test import BaseModel

# 🔑 Load key
load_dotenv()
set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# # ✅ Guardrail response format
# class MathCheck(BaseModel):
#     is_valid_math: bool
#     reason: str

# # ✅ Guardrail agent (just checks user input)
# guardrail_agent = Agent(
#     name="MathGuard",
#     instructions="Decide if the input is a math problem (like add, subtract, multiply, divide).",
#     output_type=MathCheck,
#     model=model
# )

# # ✅ Guardrail function
# @input_guardrail
# async def valid_math_input(ctx, agent, user_input: str) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, user_input, context=ctx.context)
#     validated = result.final_output_as(MathCheck)

#     return GuardrailFunctionOutput(
#         output_info=validated,
#         tripwire_triggered=not validated.is_valid_math,  # 🚨 block if false
#     )

# # ✅ Main agent (only answers math if input passes guardrail)
# math_agent = Agent(
#     name="MathAgent",
#     instructions="You are a simple math agent. Solve only math problems.",
#     model=model,
#     input_guardrails=[valid_math_input]  # attach guardrail
# )

# # ✅ Runner
# async def main():
#     try:
#         result = await Runner.run(math_agent, "What is 2 + 2?")
#         print("✅ Allowed:", result.final_output)
#     except Exception as e:
#         print("🚫 Blocked:", e)

#     try:
#         result = await Runner.run(math_agent, "Tell me a joke")
#         print("✅ Allowed:", result.final_output)
#     except Exception as e:
#         print("🚫 Blocked:", e)

# if __name__ == "__main__":
#     asyncio.run(main())

class Mathcheck(BaseModel):
    is_related_math: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail_Agent",
    instructions="Decide if the input is a math problem (like add, subtract, multiply, divide).",
    model=model,
    output_type=Mathcheck
)

@input_guardrail
async def Guardrail(ctx , user_input: str , agent)-> GuardrailFunctionOutput:
    result = await Runner.run_sync(guardrail_agent , user_input, context=ctx.context)
    validated = result.final_output_as(Mathcheck)

    return GuardrailFunctionOutput(
        output_info=validated,
        tripwire_triggered= not validated.is_related_math
    )

main_agent = Agent(
    name="Math agent",
    instructions="You are a simple math agent. Solve only math problems.",
    input_guardrails=[Guardrail]
)

async def main():
    try:
        result = await Runner.run_sync(main_agent , input="what is 2 + 2")
        return ("Allowed", result.final_output)
    except Exception as e:
        print ("Blocked", e )
    
if __name__ == '__main__':
    asyncio.run(main())