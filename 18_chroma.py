"""
Obtain data from https://sectors.app
Accompanying course material: https://sectors.app/bulletin/ai-search
"""

import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="saham")

# get it from sectors.app/idx/bbca
collection.add(
    documents=[
        "PT Alamtri Resources Indonesia Tbk (formerly PT Adaro Energy Indonesia) is engaged in comprehensive operations including mining, trading, and logistics. The company is recognized for its Envirocoal product and provides extensive support services through its subsidiaries, covering various aspects of coal mining and logistics.",
        "PT Bank Central Asia Tbk is an Indonesia-based commercial bank providing a comprehensive range of banking services, including cash management, credit facilities, and foreign exchange transactions. The bank serves corporate and retail clients across Indonesia.",
        "PT Chandra Asri Petrochemical Tbk is an integrated petrochemical company in Indonesia, primarily producing olefins and polyolefins. Its segments include Ethylene, Propylene, and various by-products produced from its Naphtha Cracker plant.",
        "PT Dharma Satya Nusantara Tbk operates in the wood processing and crude palm oil industries with CPO contributing to over 80% of its revenue.",
        "PT Asuransi Tugu Pratama Indonesia Tbk is a leading provider of general insurance and reinsurance in Indonesia, focusing on a wide range of insurance products for both corporations and individuals. The company offers short-term and long-term insurance contracts, ensuring protection against various risks such as property damage, personal accidents, and finansial losses.",
        "OCBC is a Singaporean multinational banking services corporation headquartered at the OCBC Centre. OCBC has total assets of S$581 billion at the end of 2023, making it the second largest bank in Southeast Asia by assets. It is also one of the world's most highly-rated banks, with an Aa1 rating from Moody's and AA- rating from Standard & Poor's."   
    ],
    # optional metadata:
    metadatas=[{"listed_in": "IDX", "ticker": "adro"}, {"listed_in": "IDX", "ticker": "bbca"}, {"listed_in": "IDX", "ticker": "tpia"},
                {"listed_in": "IDX", "ticker": "dsng"}, {"listed_in": "IDX", "ticker": "tugu"},  {"listed_in": "SGX", "ticker": "d05"}
              ],
    ids=["adro", "bbca", "tpia", "dsng", "tugu", "o39.si"]
)

# note that there is no mention of the word 'financial' in the documents above
# results = collection.query(
#     query_texts=["some question about financial stocks"],
#     n_results=3
# )

# results2 = collection.query(
#     query_texts=["some question about renewable energy legislation"],
#     n_results=1
# )


# print(results)
# print( " === \n " )
# print(results2)


if __name__ == "__main__":
    results3 = collection.query(
        query_texts=["some question about financial stocks"],
        where={"listed_in": "IDX"},
        n_results=2
    )

    if results3:
        header = ["ticker", "link"]
        from tabulate import tabulate
        table_data = []
        for item in results3.get('metadatas')[0]:
            ticker = item['ticker']
            listed_in = item['listed_in'].lower()
            link = f"\033]8;;https://sectors.app/{listed_in}/{ticker}\033\\{ticker} on Sectors →\033]8;;\033\\"
            table_data.append([ticker, link]) 
        print(tabulate(table_data, headers=header, tablefmt="pretty"))

    else:
        print("🤖: Can't find any matches. Try with another sector!")


