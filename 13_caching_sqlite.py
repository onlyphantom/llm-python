import time
from dotenv import load_dotenv
import langchain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.cache import SQLiteCache
from langchain.chains.summarize import load_summarize_chain

# add this to .gitignore if you don't want to commit the cache
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

load_dotenv()

text_splitter = CharacterTextSplitter()
llm = OpenAI(model_name="text-davinci-002")
no_cache_llm = OpenAI(model_name="text-davinci-002", cache=False)

with open("news/summary.txt") as f:
    news = f.read()

texts = text_splitter.split_text(news)
print(texts)

docs = [Document(page_content=t) for t in texts[:3]]

chain = load_summarize_chain(llm, chain_type="map_reduce", reduce_llm=no_cache_llm)

with get_openai_callback() as cb:
    start = time.time()
    result = chain.run(docs)
    end = time.time()
    print("--- result1")
    print(result)
    print(str(cb) + f" ({end - start:.2f} seconds)")


with get_openai_callback() as cb2:
    start = time.time()
    result = chain.run(docs)
    end = time.time()
    print("--- result2")
    print(result)
    print(str(cb2) + f" ({end - start:.2f} seconds)")
