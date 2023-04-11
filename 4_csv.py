from dotenv import load_dotenv
from langchain import OpenAI 
from langchain.document_loaders.csv_loader import CSVLoader

load_dotenv()

filepath = "academy/academy.csv"
loader = CSVLoader(filepath)
data = loader.load()
print(data)

llm = OpenAI(temperature=0)

from langchain.agents import create_csv_agent
agent = create_csv_agent(llm, filepath, verbose=True)
agent.run("What percentage of the respondents are students versus professionals?")
agent.run("List the top 3 devices that the respondents use to submit their responses")
agent.run("Consider iOS and Android as mobile devices. What is the percentage of respondents that discovered us through social media submitting this from a mobile device?")
