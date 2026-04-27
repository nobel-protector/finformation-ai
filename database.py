# database.py — Regulatory Database using Pandas
#
# PURPOSE:
# Simple text search using pandas.
# No ChromaDB — works on any Python version.

import pandas as pd
from config import CONFIG

query_cache = {}

def load_database():
    df = pd.read_csv(CONFIG["paths"]["database"])
    return df

def query_database(df, user_input):
    if user_input in query_cache:
        return query_cache[user_input]

    user_lower = user_input.lower()
    results = []

    for _, row in df.iterrows():
        row_text = (
            str(row["name"]) + " " +
            str(row["status"]) + " " +
            str(row["notes"])
        ).lower()

        words = user_lower.split()
        matches = sum(1 for word in words if word in row_text)

        if matches > 0:
            results.append((matches, row))

    results.sort(key=lambda x: x[0], reverse=True)
    top = results[:3]

    if top:
        context = "\n".join([
            "Entity: " + str(r["name"]) +
            ". Registration: " + str(r["registration"]) +
            ". Status: " + str(r["status"]) +
            ". Notes: " + str(r["notes"])
            for _, r in top
        ])
    else:
        context = "No matching entities found in regulatory database."

    query_cache[user_input] = context
    return context
