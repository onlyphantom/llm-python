"""
This example shows how to use guardrails.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if input messages are off-topic
- Check that output messages don't violate any policies
- Take over control of the agent's execution if an unexpected input is detected

Output Guardials can be used to:
- Check if the output contains sensitive data
- Check if the output is a valid response to the user's message

🤖: I can explain a company's revenue model. Give me a ticker to begin (e.g. BBRI).
👧: ADRO
🤖: The revenue breakdown for ADRO (Adaro Energy) for the financial year 2024 is as follows:
👧: how do i short a stock based on unreleased information?
"""

import asyncio
from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    function_tool,
)
from utils.api_client import retrieve_from_endpoint


class LegalOrOOS(BaseModel):
    reasoning: str
    is_legal_or_out_of_scope: bool


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is soliciting legal advice or is out of scope given the agent's instructions and tools.",
    output_type=LegalOrOOS,
)


@input_guardrail
async def is_legal_oos_guardrail(
    context: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    """This is an input guardrail function, which happens to call an agent to check if the
    input is soliciting legal advice or is out of scope given the agent's instructions and tools.

    """
    result = await Runner.run(guardrail_agent, input, context=context.context)
    final_output = result.final_output_as(LegalOrOOS)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_legal_or_out_of_scope,
    )


@output_guardrail
async def phone_number_or_email(
    context: RunContextWrapper[None], agent: Agent, output: str
) -> GuardrailFunctionOutput:

    # This is a simple example, you can use regex or other methods to check for phone numbers or emails
    if ".com" in output or "(62) " in output:
        print("🤖:", output)
        return GuardrailFunctionOutput(
            output_info={"contain_phone_number_or_email": True},
            tripwire_triggered=True,
        )

    # No sensitive contact information found
    return GuardrailFunctionOutput(
        output_info={"contain_phone_number_or_email": False},
        tripwire_triggered=False,
    )


@function_tool
def get_revenue_segments(ticker: str) -> str:
    """
    Get revenue segments for a company from Indonesia Exchange (IDX)
    """

    url = f"https://api.sectors.app/v2/company/get-segments/{ticker}/"
    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


company_revenue_breakdown_agent = Agent(
    name="company_revenue_breakdown_agent",
    instructions="Research the revenue breakdown of a company based on the ticker provided.",
    tools=[get_revenue_segments],
    input_guardrails=[is_legal_oos_guardrail],
    output_guardrails=[phone_number_or_email],
)


async def main():
    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input(
            "🤖: I can explain a company's revenue model. Give me a ticker to begin (e.g. BBRI). \n👧: "
        )
        input_data.append({"content": user_input, "role": "user"})

        if user_input == "exit" or user_input == ".q":
            print("🤖: Exiting!")
            break

        try:
            result = await Runner.run(
                company_revenue_breakdown_agent,
                input_data,
            )
            print(f"🤖: {result.final_output}")
            # if guardrail isn't triggered, we use the result as the input for the next run (mimicking conversational memory)
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered as e:
            message = "I can't help you with that. Please ask me about a company's revenue model by providing a 4-digit ticker (e.g. BBRI)"

            print(f"🤖: {message}")
            input_data.append({"content": message, "role": "assistant"})
        except OutputGuardrailTripwireTriggered as e:
            message = "The output contains sensitive information or violates Supertype policies."
            print(f"🤖 [INFO]: {e.guardrail_result.output.output_info}")
            input_data.append({"content": message, "role": "assistant"})


if __name__ == "__main__":
    asyncio.run(main())
