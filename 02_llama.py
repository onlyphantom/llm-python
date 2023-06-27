from dotenv import load_dotenv
load_dotenv()

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.graph_stores import SimpleGraphStore

documents = SimpleDirectoryReader('news').load_data()

index = GPTVectorStoreIndex.from_documents(documents)

# save to disk
index.storage_context.persist()

# load from disk
storage_context = StorageContext(
    docstore=SimpleDocumentStore.from_persist_dir('storage'),
    vector_store=SimpleVectorStore.from_persist_dir('storage'),
    index_store=SimpleIndexStore.from_persist_dir('storage'),
    graph_store=SimpleGraphStore.from_persist_dir('storage')
)
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
r = query_engine.query("Who are the main exporters of Coal to China? What is the role of Indonesia in this?")
print(r)
