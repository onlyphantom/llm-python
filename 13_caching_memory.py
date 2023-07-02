"""
LangChain has an incredible caching system layered on top of the Large Languange Models 
(LLMs) that you use it with. The resources on this though are pretty scarce, and as of this
recording, many of them are still outdated. If you search its official documentation, you will see it still
uses the old .predict() and if you try to run it, you'll get issues like this https://github.com/hwchase17/langchain/issues/6740
and it doesn't run. I did a quick google search and checked the first two results and they are
just lazy copy-and-paste from the docs, which means it's also wrong and plainly doesn't work.

But caching is so, so useful. Especially if you're building LLMs for production use where you're feeding
a large context to the model, like using GPT to query your own personal knowledge base (I have a video
on exactly that where I load in my bullet journals in a markdown format and build my query engine using gpt on top of it),
or if you're trying to learn a foreign language by getting GPT to tutor you on a 
book (also have a video on that). In both cases, you're feeding a large context to the model, and you
are going to incur quite a bit of cost and your queries will be slow if you don't cache.

So let me show you how to Caching with langchain and it's surprisingly easy. All of this code will be
on my github, along with the rest of this LLM series if you've been following along. We're on video number
13 now so there's a lot we've covered, and caching is just a great addition to your LLM development toolkit.

Let's open up a file and start with langchain's implementation of an in memory cache. Name it demo whatever. 
Before looking at the code, if you had asked me to guess, I thought it would be using
python's LRU cache, which is also part of the standard library. I love caching and I have a video on LRU
cache if you want to introduce built in caching to your python programs. But I took at the code and
realize I was wrong, it was far simpler than that, it's just a dictionary. https://github.com/hwchase17/langchain/blob/master/langchain/cache.py#L102

And as a quick primer, a cache is just this dictionary that stores the result of a function call, 
so that repeated calls with the same arguments don't have to recompute the result. So if you have a
function that takes a long time to run, you can cache the result of that function call, and the next
time you use the input it should yield the same result by just referring to the dictionary, do a quick
look up instead of burning your openai credits, your computation power, or whatever resource you're using
for the computation. It saves you lots of time and money, and if you're not using cache for all these 
repeated queries, you're leaving money on the table.
"""

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
