from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

load_dotenv()

# dburi = os.getenv("DATABASE_URL")
dburi = "sqlite:///academy/academy.db"
db = SQLDatabase.from_uri(dburi)
llm = OpenAI(temperature=0)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

db_chain.run("How many rows is in the responses table of this db?")
db_chain.run("Describe the responses table")
db_chain.run("What are the top 3 countries where these responses are from?")
db_chain.run("Give me a summary of how these customers come to hear about us. \
    What is the most common way they hear about us?")
