import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["skillgap_database"]
collection = db["industry_skills"]

print("🔄 Loading industry dataset...")

# Load CSV
df = pd.read_csv("processed_industry_skills.csv")

# Keep only required columns
df = df[["Domain", "clean_skill"]]

# Rename for consistency
df.columns = ["domain", "skill"]

# Convert to dictionary
data = df.to_dict(orient="records")

# Clear old data
collection.delete_many({})

# Insert new data
collection.insert_many(data)

print("✅ Industry skills inserted successfully!")