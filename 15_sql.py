"""
Obtain data from https://sectors.app
Accompanying course material: https://sectors.app/bulletin/ai-search
"""

import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
import os
# from langchain_deepseek import ChatDeepSeek

if not os.path.exists('industry.db'):
    print("Creating industry.db")
    df = pd.read_csv('./datasets/industry-leaders-full.csv')
    engine = create_engine('sqlite:///industry.db')
    df.to_sql("industry", engine, index=False, if_exists='replace')

else:
    # connect to the existing database, dont create
    engine = create_engine('sqlite:///industry.db')

db = SQLDatabase(engine=engine)


print(db.get_usable_table_names())

# query = "SELECT * FROM industry WHERE sub_industry LIKE '%banks%'"
query2 = "SELECT * FROM industry WHERE total_market_cap > 1e14"
print(db.run(query2))

llm = ChatGroq(
    model_name="llama3-70b-8192"
)

# llm = ChatDeepSeek(
#     model="deepseek-chat"
# )

agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
agent_executor.invoke({
    "input": "what are the top market cap gainers for companies in the coal industry? Return in markdown table."
})