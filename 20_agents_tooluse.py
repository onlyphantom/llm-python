import os
import json
import requests
from typing import List
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")


headers = {"Authorization": SECTORS_API_KEY}


def retrieve_from_endpoint(url: str) -> dict:

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return json.dumps(data)


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
    limit: int = 10,
    offset: int = 0,
) -> List[dict]:
    """
    Get companies matching user screening criteria from Indonesia Exchange (IDX).

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


company_research_agent = Agent(
    name="company_research_agent",
    instructions="Research the company based on the ticker provided.",
    tools=[get_company_overview, company_screener],
    tool_use_behavior="run_llm_again",
)


async def main():
    query = "Tell me about the company listed on Singapore Exchange with ticker 'D05'."
    result = await Runner.run(company_research_agent, query)
    print(f"👧: {query}")
    print(f"🤖: {result.final_output}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
