from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from dotenv import load_dotenv

load_dotenv()

documents = SimpleDirectoryReader('news').load_data()

index = GPTSimpleVectorIndex.from_documents(documents)

# save to disk
index.save_to_disk('index.json')
# load from disk
index = GPTSimpleVectorIndex.load_from_disk('index.json')

r = index.query("Who are the main exporters of Coal to China? What is the role of Indonesia in this?")
print(r)
