from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()
embeddings = OpenAIEmbeddings()
text = "Algoritma is a data science school based in Indonesia"
doc_embeddings = embeddings.embed_documents([text])

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# print(OPENAI_API_KEY)
print(doc_embeddings)
