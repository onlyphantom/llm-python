"""
This example demonstrates a deterministic flow, where each step is performed by an agent.

Usage:
python 3_deterministic.py
🤖: What kind of companies are you interested in?
👧: companies with the largest market cap
"""

import asyncio
import json
import urllib.parse

from pydantic import BaseModel
from typing import List
from agents import Agent, Runner, function_tool, trace
from utils.api_client import retrieve_from_endpoint
from datetime import datetime


@function_tool
def get_company_overview(ticker: str, country: str) -> str:
    """
    Get company overview from Singapore Exchange (SGX) or Indonesia Exchange (IDX)
    """
    assert country.lower() in [
        "indonesia",
        "singapore",
        "malaysia",
    ], "Country must be either Indonesia, Singapore, or Malaysia"

    if country.lower() == "indonesia":
        url = f"https://api.sectors.app/v2/company/report/{ticker}/?sections=overview"
    if country.lower() == "singapore":
        url = f"https://api.sectors.app/v2/sgx/company/report/{ticker}/"
    if country.lower() == "malaysia":
        url = f"https://api.sectors.app/v2/klse/company/report/{ticker}/"

    try:
        return retrieve_from_endpoint(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


@function_tool
def company_screener(
    q: str = None,
    where: str = None,
    order_by: str = None,
    desc: bool = False,
    limit: int = 3,
    offset: int = 0,
) -> List[dict]:
    """
    Get companies matching user screening criteria from Indonesia Exchange (IDX).
    Returns a list of companies, each with a symbol (e.g. "BBCA.JK") and company_name.

    Args:
        q: A natural language question. If the user gives screening criteria in natural language, compose them as a SENTENCE (not as a SQL query) and send it as this parameter, including the number of results wanted, e.g. "top 3 companies by market cap". When q is given, the API parses it with an LLM and ignores all other params. Do not try to transform the user query into SQL-like queries, the API will handle it.
        where: A filter query to screen companies based on specific field values.
               Example: "market_cap > 1000000000000 AND sector = 'Financials'"
        order_by: The field to sort the results by. Prefix with "-" for descending.
                  Example: "-market_cap"
        desc: Set to True for descending order, False for ascending.
        limit: The number of results to return.
        offset: The starting position for pagination.
    """
    base_url = "https://api.sectors.app/v2/companies/"
    params = {}

    # Per API design, if 'q' is present, it takes precedence and other filters are ignored.
    if q:
        params["q"] = q
    else:
        # Build the structured query only if 'q' is not provided.
        if where:
            params["where"] = where
        if order_by:
            params["order_by"] = order_by
        if desc:
            params["desc"] = "true"
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

    # Construct the full URL with properly encoded parameters
    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}"
    else:
        # Handles the case where no parameters are given at all
        url = base_url

    try:
        # retrieve_from_endpoint returns a JSON string, so parse it before reading "results"
        response = json.loads(retrieve_from_endpoint(url))
        return response.get("results", [])
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


@function_tool
def csv_export(data: object) -> str:
    """
    Convert the object to a csv
    """
    import pandas as pd

    # Convert the object to a DataFrame
    df = pd.DataFrame.from_dict(data, orient="index")

    # Convert the DataFrame to a CSV saved as 'export.csv'
    df.to_csv("export.csv", index=True)
    return "Successfully exported to export.csv"


class ValidTickers(BaseModel):
    tickers: List[str]


get_top_companies_based_on_metric = Agent(
    name="get_top_companies_based_on_metric",
    instructions=(
        "Get the top companies based on the given metric using the company_screener tool. "
        "Return 3 companies unless the user asks for a different number. "
        "Return the tickers of the top companies, without the .JK suffix. Return in a List."
    ),
    tools=[company_screener],
    output_type=List[str],
)

determine_companies_to_research = Agent(
    name="determine_companies_to_research",
    instructions="Generate a list of tickers (symbols) of companies to research based on the query. Tickers on IDX are exactly 4 characters long, e.g. BBCA, BBRI, TKLM",
    output_type=ValidTickers,
)

company_research_agent = Agent(
    name="company_research_agent",
    instructions="Research each company of a given list using the assigned tool, always assume indonesian companies unless otherwise specified.",
    tools=[get_company_overview],
    output_type=str,
)


async def main():
    input_prompt = input(f"🤖: What kind of companies are you interested in? \n👧: ")
    # Ensure the entire workflow is a single trace
    with trace("Deterministic research flow"):
        # 1. Determine the companies ranked by certain dimension
        top_companies_ranked = await Runner.run(
            get_top_companies_based_on_metric, input_prompt
        )
        print("🤖:", top_companies_ranked.final_output)

        # 2. Add a gate to stop if the tickers are not valid
        assert isinstance(top_companies_ranked.final_output, list), "Invalid tickers"

        # 3. Research the company based on the query
        # 3.1 Append to Notes
        with open("3_research_notes.txt", "a") as f:
            f.write(f"Research on {input_prompt}:\n")
            f.write(f"Top companies: {top_companies_ranked.final_output}\n\n\n")

            for ticker in top_companies_ranked.final_output:
                print(f"🤖: Getting information on: {ticker}")
                company_research_result = await Runner.run(
                    company_research_agent, ticker
                )
                if (
                    not company_research_result
                    or not company_research_result.final_output
                ):
                    print(f"🤖: Failed to get data for {ticker}")
                    f.write(f"❌ Failed to get data for {ticker}\n")
                    continue
                print(f"🤖: {company_research_result.final_output}")
                f.write(f"Company: {ticker}\n")
                f.write(
                    ""
                    + company_research_result.final_output
                    + "\n\n"
                    + "Research Date: "
                    + datetime.now().isoformat()
                    + "\n\n\n"
                )

        print(f"🤖: Done! I have provided the information on: {input_prompt}")


if __name__ == "__main__":
    asyncio.run(main())
