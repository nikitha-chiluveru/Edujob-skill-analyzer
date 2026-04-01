import pandas as pd
import re

# Load CBIT CSV
df = pd.read_csv("cbit syllabus.csv", encoding="utf-8", engine="python")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Fix encoding garbage
    text = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")

    # Remove college repeated name
    text = re.sub(r'Chaitanya Bharathi Institute of Technology.*?INFORMATION TECHNOLOGY', '', text, flags=re.IGNORECASE)

    # Remove Text Book / Suggested Reading / Web Resources
    text = re.sub(r'Text Book:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Suggested Reading:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Web Resources:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COURSE OUTCOMES:.*', '', text, flags=re.IGNORECASE)

    # Remove UNIT labels
    text = re.sub(r'UNIT\s*[-–]?\s*[IVX0-9]+:?', '', text, flags=re.IGNORECASE)

    # Replace weird separators
    text = text.replace("|", ",")
    text = text.replace("â€“", "-")
    text = text.replace("â€™", "'")
    text = text.replace("â€œ", '"').replace("â€", '"')

    # Remove multiple commas
    text = re.sub(r',+', ',', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Clean leading/trailing commas and spaces
    text = text.strip(" ,")

    return text


# Clean only Topics Covered column
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove completely empty topic rows
df = df[df["Topics Covered"] != ""]

# Save cleaned file
df.to_csv("cbit_cleaned_proper.csv", index=False)

print("✅ CBIT file cleaned properly!")
