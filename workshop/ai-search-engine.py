import os
from typing import List
import requests
import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

llm = ChatGroq(model="llama3-8b-8192")

def retrieve_from_endpoint(url: str) -> dict:
    headers = {"Authorization": SECTORS_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return json.dumps(data)

@tool
def get_company_overview(stock: str) -> str:
    """
    Get company overview, enter stock code (e.g BBRI, TLKM)
    """

    url = f"https://api.sectors.app/v1/company/report/{stock}/?sections=overview"

    return retrieve_from_endpoint(url)

@tool
def get_sector_overview(sector: str) -> str:
    """
    Get sector overview, enter sector name (e.g banks, housing estate development)
    """

    url = f"https://api.sectors.app/v1/subsector/report/{sector}/"

    return retrieve_from_endpoint(url)

def get_all_valid_subsector_slugs() -> str:
    """
    Get all valid subsector slugs
    """

    url = "https://api.sectors.app/v1/subsectors/"

    return retrieve_from_endpoint(url)

def match_input_to_valid_subsector_slug(
        valid_subsector_slugs: List[str],
        user_input: str,
        fuzzy_threshold: int = 80,
        ) -> str:
    """
    Match input to valid subsector slug
    """
    from fuzzywuzzy import fuzz
    
    good_approximation = []
    # Challenge (1) implement this here

    return good_approximation


tools = [
    get_company_overview, 
    get_sector_overview,
    # ... other tools
]

memory = MemorySaver()
system_message = "You are an expert tool calling agent meant for financial data retriever and summarization. Use tools to get the information you need, be descriptive, insightful and use the data you get to make high quality commentary."

app = create_react_agent(llm, 
    tools, 
    state_modifier=system_message, 
    checkpointer=memory
)


def chat(session_id: str, input: str) -> str:
    out = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content=input,
                    session_id=session_id,
                )
            ]
        },
        config={"configurable": {"thread_id": "supertype"}},
    )
    return f'🤖: {out["messages"][-1].content}'

if __name__ == "__main__":

    valid_subsector_slugs = get_all_valid_subsector_slugs()
    subsector_slugs = [item.get('subsector') for item in eval(valid_subsector_slugs)]

    user_input = input("→: Enter a sector name (e.g. 'banks')  or 4-digit ticker (e.g 'bmri'). Enter .q to exit. \n→: ")
    # Challenge (2) implement the fuzzy search here 

    out = chat("supertype", f"Give me a company overview of {user_input}")
    print(out)




