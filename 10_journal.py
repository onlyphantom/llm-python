from dotenv import load_dotenv
load_dotenv()

import argparse
import logging
import sys
from pathlib import Path
from llama_index import (
    ObsidianReader, 
    GPTVectorStoreIndex,
    StorageContext,
    load_index_from_storage
)

# to see token counter and token usage for the LLM and Embedding
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


OBSIDIAN_DIR = "/home/samuel/vaults/fragments/journals"
docs = ObsidianReader(OBSIDIAN_DIR).load_data()


def read_journal_md(file_path):
    from bs4 import BeautifulSoup
    import markdown
    import re
    
    with open(file_path, "r") as f:
            text = f.read()
            html = markdown.markdown(text)
            soup = BeautifulSoup(html, "html.parser")

            # take only the first <p> tag
            # p = soup.find("p")
            ps = soup.find_all("p")
            # take only the p tags that have at least 2 `|` characters
            p = [p for p in ps if p.text.count("|") > 1]

            # replace all characters before the first `|` character with ''
            result = re.sub(r'^[^|]*\|', '', p[0].text)

            print(f"Finished processing {file_path}")
    return result


def create_journal_nodes(dir_path):
    """
    Examples: https://gpt-index.readthedocs.io/en/stable/guides/primer/usage_pattern.html
    """
    from llama_index import Document
    from llama_index.node_parser import SimpleNodeParser


    docs = []
    parser = SimpleNodeParser()

    # loop through each markdown file in the directory
    for file_path in Path(dir_path).glob("*.md"):
        md = read_journal_md(file_path)
        # construct documents manually using the lower level Document struct
        docs.append(Document(md))
        
    nodes = parser.get_nodes_from_documents(docs)


    return nodes, docs

if Path("./storage").exists():
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
else:
    nodes, docs = create_journal_nodes(OBSIDIAN_DIR)
    index = GPTVectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir="./storage")

if __name__ == "__main__":
    """
    Usage: python 10_journal_x.py -q "what are places I ate at in March and April?"
    """
    query_engine = index.as_query_engine()
    # cli argument parser
    parser = argparse.ArgumentParser(
        prog="QueryJournal",
        description="Query my bullet journals in Obsidian using Llama Index."
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Ask a question answerable in my journals",
        required=True
    )
    args = parser.parse_args()
    query = args.query

    if(query):
        res = query_engine.query(query)
        print(f"Query: {query}")
        print(f"Results: \n {res}")
    else:
        print("No query provided. Exiting...")
        exit(0)
