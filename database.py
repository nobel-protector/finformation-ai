# database.py — ChromaDB loading and querying
#
# PURPOSE:
# This file handles all communication with the regulatory database.
# Think of it as the LIBRARIAN of Finformation.ai.
#
# WHAT IT DOES:
# 1. Reads regulatory_database.csv
# 2. Loads all 100 entities into ChromaDB
# 3. Searches ChromaDB for relevant records
# 4. Caches results for faster repeated queries

import chromadb
import pandas as pd
from config import CONFIG

# Simple cache to avoid repeated queries
query_cache = {}

def load_database():
    df = pd.read_csv(CONFIG["paths"]["database"])
    chroma_client = chromadb.Client()
    try:
        chroma_client.delete_collection("regulatory_data")
    except:
        pass
    collection = chroma_client.get_or_create_collection("regulatory_data")
    for i, row in df.iterrows():
        name = str(row["name"])
        reg = str(row["registration"])
        regulator = str(row["regulator"])
        status = str(row["status"])
        notes = str(row["notes"])
        doc = "Entity: " + name + ". Registration: " + reg + ". Regulator: " + regulator + ". Status: " + status + ". Notes: " + notes
        collection.add(documents=[doc], ids=[str(i)])
    return collection

def query_database(collection, user_input):
    if user_input in query_cache:
        return query_cache[user_input]
    results = collection.query(
        query_texts=[user_input],
        n_results=CONFIG["max_db_results"]
    )
    context = "\n".join(results["documents"][0])
    query_cache[user_input] = context
    return context
