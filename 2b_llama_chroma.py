from llama_index import GPTChromaIndex, SimpleDirectoryReader
import chromadb

from dotenv import load_dotenv

load_dotenv()
#  https://docs.trychroma.com/embeddings
# create a Chroma vector store, by default operating purely in-memory
chroma_client = chromadb.Client()

# create a collection
chroma_collection = chroma_client.create_collection("newspieces")
# https://docs.trychroma.com/api-reference
print(chroma_collection.count())

documents = SimpleDirectoryReader('news').load_data()

index = GPTChromaIndex.from_documents(documents, chroma_collection=chroma_collection)
print(chroma_collection.count())
print(chroma_collection.get()['documents'])
print(chroma_collection.get()['metadatas'])

index.save_to_disk("newspieces.json")

# During query time, the index uses Chroma to query for the top k
# most similar nodes, and synthesizes an answer from the retrieved nodes.

r = index.query("Who are the main exporters of Coal to China? What is the role of Indonesia in this?")
print(r)
