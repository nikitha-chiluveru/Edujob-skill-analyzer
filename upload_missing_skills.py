import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["skill_gap_project"]
collection = db["domain_missing_skills"]

df = pd.read_csv("semantic_missing_skills.csv")

data = df.to_dict("records")

collection.delete_many({})
collection.insert_many(data)

print("Missing skills inserted successfully!")