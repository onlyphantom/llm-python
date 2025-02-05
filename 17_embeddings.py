"""
Obtain data from https://sectors.app
Accompanying course material: https://sectors.app/bulletin/ai-search
"""

import numpy as np
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAIEmbeddings
embed = OpenAIEmbeddings()

input_text = "supertype financial statements?"
input_docs = ["financial_algoritma", 
    "annual_report_algoritma", 
    "financial_supertype", 
    "agm_supertype", 
    "egm_supertype",
    "financial_hypergrowth", 
    "annual_report_hypergrowth", 
    "agm_sectors",
    "financial_statements_template"
]

query = embed.embed_query(input_text)
docs = embed.embed_documents(input_docs)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

similarities = [cosine_similarity(query, doc) for doc in docs]

for i, sim in enumerate(similarities):
    print(f"Cosine Similarity with doc {i}: {sim}")

most_similar_index = np.argmax(similarities)
print(f"Document: {input_docs[most_similar_index]}") 
