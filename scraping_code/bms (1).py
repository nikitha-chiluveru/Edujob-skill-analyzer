import pandas as pd
import re

# Load CSV
df = pd.read_csv("bms_college_syllabus.csv")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # 1️⃣ Remove UNIT (Roman + numeric)
    text = re.sub(r'UNIT\s*[IVXLCDM\d]+\s*:?', '', text, flags=re.IGNORECASE)

    # 2️⃣ Remove Course Outcomes (CO1, CO2 etc)
    text = re.sub(r'CO\d+', '', text)

    # 3️⃣ Remove ISBN, Edition, Publication lines
    text = re.sub(r'ISBN.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Edition.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Publication.*', '', text, flags=re.IGNORECASE)

    # 4️⃣ Replace separators with comma
    text = re.sub(r'\|', ',', text)
    text = re.sub(r':', ',', text)
    text = re.sub(r'–', ',', text)
    text = re.sub(r'-', ',', text)
    text = re.sub(r';', ',', text)
    text = re.sub(r'\n', ',', text)

    # 5️⃣ Remove unwanted special characters
    text = re.sub(r'[^a-zA-Z0-9,\s]', ' ', text)

    # 6️⃣ Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # 7️⃣ Split into topics
    parts = [p.strip() for p in text.split(",")]

    clean_list = []

    for p in parts:

        # Remove unwanted heading-like words
        if p.lower().startswith((
            "introduction",
            "overview",
            "case study",
            "reference",
            "course outcomes",
            "basic concepts"
        )):
            continue

        # Keep only meaningful topic phrases
        if 5 < len(p) < 70:
            clean_list.append(p)

    # Remove duplicates while preserving order
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)


# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Save cleaned file
df.to_csv("bms_college_syllabus_cleaned.csv", index=False)

print("✅ Cleaning Completed Successfully.")
