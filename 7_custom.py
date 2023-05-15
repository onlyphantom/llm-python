"""
Optional: Change where pretrained models from huggingface will be downloaded (cached) to:
export TRANSFORMERS_CACHE=/whatever/path/you/want
"""

# import os
# os.environ["TRANSFORMERS_CACHE"] = "/media/samuel/UDISK1/transformers_cache"
import os
import time

import torch
from dotenv import load_dotenv
from langchain.llms.base import LLM
from llama_index import (
    GPTListIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
    SimpleDirectoryReader,
)
from transformers import pipeline

# load_dotenv()
os.environ["OPENAI_API_KEY"] = "random"


def timeit():
    """
    a utility decoration to time running time
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            args = [str(arg) for arg in args]

            print(f"[{(end - start):.8f} seconds]: f({args}) -> {result}")
            return result

        return wrapper

    return decorator


prompt_helper = PromptHelper(
    # maximum input size
    max_input_size=2048,
    # number of output tokens
    num_output=256,
    # the maximum overlap between chunks.
    max_chunk_overlap=20,
)


class LocalOPT(LLM):
    # model_name = "facebook/opt-iml-max-30b" (this is a 60gb model)
    model_name = "facebook/opt-iml-1.3b"  # ~2.63gb model
    # https://huggingface.co/docs/transformers/main_classes/pipelines
    pipeline = pipeline(
        "text-generation",
        model=model_name,
        device="cuda:0",
        model_kwargs={"torch_dtype": torch.bfloat16},
    )

    def _call(self, prompt: str, stop=None) -> str:
        response = self.pipeline(prompt, max_new_tokens=256)[0]["generated_text"]
        # only return newly generated tokens
        return response[len(prompt) :]

    @property
    def _identifying_params(self):
        return {"name_of_model": self.model_name}

    @property
    def _llm_type(self):
        return "custom"


@timeit()
def create_index():
    print("Creating index")
    # Wrapper around an LLMChain from Langchaim
    llm = LLMPredictor(llm=LocalOPT())
    # Service Context: a container for your llamaindex index and query
    # https://gpt-index.readthedocs.io/en/latest/reference/service_context.html
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm, prompt_helper=prompt_helper
    )
    docs = SimpleDirectoryReader("news").load_data()
    index = GPTListIndex.from_documents(docs, service_context=service_context)
    print("Done creating index", index)
    return index


@timeit()
def execute_query():
    response = index.query(
        "Who does Indonesia export its coal to in 2023?",
        # This will preemptively filter out nodes that do not contain required_keywords
        # or contain exclude_keywords, reducing the search space and hence time/number of LLM calls/cost.
        exclude_keywords=["petroleum"],
        # required_keywords=["coal"],
        # exclude_keywords=["oil", "gas", "petroleum"]
    )
    return response


if __name__ == "__main__":
    """
    Check if a local cache of the model exists,
    if not, it will download the model from huggingface
    """
    if not os.path.exists("7_custom_opt.json"):
        print("No local cache of model found, downloading from huggingface")
        index = create_index()
        index.save_to_disk("7_custom_opt.json")
    else:
        print("Loading local cache of model")
        llm = LLMPredictor(llm=LocalOPT())
        service_context = ServiceContext.from_defaults(
            llm_predictor=llm, prompt_helper=prompt_helper
        )
        index = GPTListIndex.load_from_disk(
            "7_custom_opt.json", service_context=service_context
        )

    response = execute_query()
    print(response)
    print(response.source_nodes)
