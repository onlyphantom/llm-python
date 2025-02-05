"""
Obtain data from https://sectors.app
Accompanying course material: https://sectors.app/bulletin/ai-search

Easily generalizes to multiple csvs, or sqlites since we just load
them into one table

- this is how GPT-4o-turbo cheat in the gun-to-knife-fight:
- https://sectors.app/bulletin/deepseek

Usage: python pre/repl.py
    -  sub-industries in our df where the parent industry is coal-related
    - industries in our db with more than 45 total number of companies
    - top 5 largest industries in our db by sum of market cap
"""
import os

from dotenv import load_dotenv
import pandas as pd

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser


load_dotenv()
SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")

df = pd.read_csv('./datasets/industry-leaders-full.csv')

industry = df.loc[:, ['industry', 'sub_industry', 'total_market_cap', 'num_of_companies']]

python_repl = PythonAstREPLTool(locals={"df": industry})

llm = ChatGroq(
    model_name="llama3-70b-8192"
)

system_prompt = f""" Here is the output of `df.head().to_markdown()`: \\
\\`\\`\\`
{industry.head().to_markdown()}
\\`\\`\\`
top_mcap_gainers are for Top Market Cap Gainers; Use Python code to answer whenever possible. Answer with pretty print and in tabular format as much as possible, in the neatest way possible.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

tools = [
    python_repl
]

llm_with_tools = llm.bind_tools(tools, tool_choice=python_repl.name)
parser = JsonOutputKeyToolsParser(key_name=python_repl.name, first_tool_only=True)

if __name__ == "__main__":
    query_string = input("🤖: Enter a query: ")
    # the last python_repl tool is the one that will be used to execute python code
    # remove it if you want to see what it will execute but not actually execute it
    # chain = prompt | llm_with_tools | parser
    chain = prompt | llm_with_tools | parser | python_repl
    response = chain.invoke({"input": query_string})
    print(response)
    