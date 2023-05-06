import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    GPTVectorStoreIndex,
    QuestionAnswerPrompt,
)
import pinecone
from llama_index.vector_stores import PineconeVectorStore
from llama_index.storage.storage_context import StorageContext
from langchain.chat_models import ChatOpenAI

load_dotenv()

urls = [
    "https://www.projekt-gutenberg.org/nietzsch/wanderer/wanderer.html",
    "https://www.projekt-gutenberg.org/nietzsch/wanderer/wande002.html",
    "https://www.projekt-gutenberg.org/nietzsch/wanderer/wande003.html",
    "https://www.projekt-gutenberg.org/nietzsch/wanderer/wande004.html"
]

def create_pages(urls):
    
    pages = []
    for url in urls:
        pagename = url.split("/")[-1]
        pages.append(pagename)
    
    return pages


def scrape_book(urls):
    from pathlib import Path
    result = []
    
    for url in urls:

        req = requests.get(url)
        soup = BeautifulSoup(
            req.text, 
            "html.parser",
        )

        # keep only the heading tags and <p> tags
        text = soup.find_all(["h1", "h2", "h3", "p"])

        # remove the tags and keep only the text
        text = [t.text for t in text]

        for i in text:
            try:
                result.append(i.encode('latin').decode("utf-8"))
            except:
                pass

        book_path = Path("book")
        if not book_path.exists():
            book_path.mkdir()

        pagename = url.split("/")[-1]

        with open(book_path / f"{pagename}.txt", "w") as f:
            f.write("\n".join(result))
    
    return result


def build_docs(pages):
    docs = {}
    for page in pages:
        docs[page] = SimpleDirectoryReader(
            input_files=[f"book/{page}.txt"]
        ).load_data()
    return docs

def build_context(model_name):
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(temperature=0, model_name=model_name)
    )
    return ServiceContext.from_defaults(llm_predictor=llm_predictor)

def build_index(pages, docs):

    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment="us-west4-gcp"
    )
    pinecone.create_index("nietzsche", dimension=1536, metric="cosine")
    pinecone_index = pinecone.Index("nietzsche")

    service_context = build_context("gpt-3.5-turbo")

    pages_indexes = {}
    for page in pages:
        metadata_filters = {"page": page}
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index,
            metadata_filters=metadata_filters
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        pages_indexes[page] = GPTVectorStoreIndex.from_documents(
            docs[page], storage_context=storage_context, service_context=service_context
        )
        pages_indexes[page].index_struct.index_id = page

    print("Indexing complete.")
    return pages_indexes

def create_query_engine(chapter="wande002.html"):
    
    PROMPT_TEMPLATE = (
        "Here are the context information:"
        " \n----------------------------------\n"
        "{context_str}"
        " \n----------------------------------\n"
        "Answer the following question in the original german text, then provide an english translation and explanation in as instructive and educational way as possible: {query_str}\n"
    )
    QA_PROMPT = QuestionAnswerPrompt(PROMPT_TEMPLATE)

    query_engine = indices[chapter].as_query_engine(
        text_qa_template=QA_PROMPT
    )
    return query_engine

if __name__ == "__main__":
    # scrape_book(urls)
    pages = create_pages(urls)
    docs = build_docs(pages) # print(docs.keys())
    indices = build_index(pages, docs)

    query_engine = create_query_engine(chapter="wande002.html")
    response = query_engine.query("what are important things according to Nietzsche?")

    print(str(response))
    print(response.get_formatted_sources())
