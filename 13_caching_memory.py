import time
from dotenv import load_dotenv
import langchain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.cache import InMemoryCache

load_dotenv()

# to make caching obvious, we use a slow model
llm = OpenAI(model_name="text-davinci-002")

langchain.llm_cache = InMemoryCache()

with get_openai_callback() as cb:
    start = time.time()
    result = llm("What doesn't fall far from the tree?")
    print(result)
    end = time.time()
    print("--- cb")
    print(str(cb) + f" ({end - start:.2f} seconds)")

with get_openai_callback() as cb2:
    start = time.time()
    result2 = llm("What doesn't fall far from the tree?")
    result3 = llm("What doesn't fall far from the tree?")
    end = time.time()
    print(result2)
    print(result3)
    print("--- cb2")
    print(str(cb2) + f" ({end - start:.2f} seconds)")
