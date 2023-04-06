import os 
from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase
from langchain import SQLDatabaseChain

load_dotenv()

dburi = os.getenv("DATABASE_URL")
db = SQLDatabase.from_uri(dburi)
llm = OpenAI(temperature=0)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

db_chain.run("How many responses do we have this year?")
db_chain.run("What is the average ratings for Samuel Chan in the responses table?")
