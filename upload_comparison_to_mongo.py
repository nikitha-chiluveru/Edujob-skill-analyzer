import pandas as pd
from pymongo import MongoClient

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["skill_gap_project"]
collection = db["domain_comparison"]

print("Connected to MongoDB")

# 2️⃣ Load CSV file
df = pd.read_csv("semantic_domain_gap_report.csv")

print("CSV Loaded Successfully")

# 3️⃣ Convert dataframe to dictionary format
data = df.to_dict("records")

# 4️⃣ Clear old records (so it doesn't duplicate)
collection.delete_many({})

# 5️⃣ Insert into MongoDB
collection.insert_many(data)

print("✅ Comparison data inserted into MongoDB successfully!")