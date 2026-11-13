"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.

# Usage:
🤖: I'm a financial report research analyst. Enter a stock ticker on IDX to begin.
👧: ADRO
"""

import asyncio

from agents import Agent, Runner, ItemHelpers, function_tool, trace
from utils.api_client import retrieve_from_endpoint


@function_tool
def get_company_financials(ticker: str) -> str:
    """
    Get company financials from Indonesia Exchange (IDX)
    """
    url = f"https://api.sectors.app/v2/company/report/{ticker}/?sections=financials"
    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


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


@function_tool
def get_quarterly_financials(ticker: str) -> str:
    """
    Get revenue segments for a company from Indonesia Exchange (IDX)
    """

    url = f"https://api.sectors.app/v2/financials/quarterly/{ticker}/?report_date=2024-12-31&approx=true"
    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


company_financials_research_agent = Agent(
    name="company_financials_research_agent",
    instructions="Research the financials of a company based on the ticker provided.",
    tools=[get_company_financials],
    output_type=str,
)

company_revenue_breakdown_agent = Agent(
    name="company_revenue_breakdown_agent",
    instructions="Research the revenue breakdown of a company based on the ticker provided.",
    tools=[get_revenue_segments],
    output_type=str,
)

company_quarterly_financials_agent = Agent(
    name="company_quarterly_financials_agent",
    instructions="Research the quarterly financials of a company based on the ticker provided.",
    tools=[get_quarterly_financials],
    output_type=str,
)

research_team_leader_aggregator = Agent(
    name="research_team_leader_aggregator",
    instructions="You are the team leader of a research team. You will aggregate the results from these agents and provide a consolidated answer that is relevant to the user.",
    output_type=str,
)


async def main():
    input_prompt = input(
        f"🤖: I'm a financial report research analyst. Enter a stock ticker on IDX to begin. \n👧: "
    )

    # Ensure the entire workflow is a single trace
    with trace("Parallelization"):
        # Run the agents in parallel
        agent_res1, agent_res2, agent_res3 = await asyncio.gather(
            Runner.run(company_financials_research_agent, input_prompt),
            Runner.run(company_revenue_breakdown_agent, input_prompt),
            Runner.run(company_quarterly_financials_agent, input_prompt),
        )
        outputs = [
            ItemHelpers.text_message_outputs(agent_res1.new_items),
            ItemHelpers.text_message_outputs(agent_res2.new_items),
            ItemHelpers.text_message_outputs(agent_res3.new_items),
        ]

        # Aggregate the results
        aggregated_result = "\n\n".join(outputs)

        summary = await Runner.run(research_team_leader_aggregator, aggregated_result)

        print(f"🤖: {summary.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
