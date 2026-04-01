import pandas as pd
import re

# Load file
df = pd.read_excel("KIIT_Fixed_Output.xlsx")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # 🔥 Remove ALL UNIT patterns (Roman + numbers + with/without colon)
    text = re.sub(r'UNIT\s*[IVXLCDM\d]+\s*:?', '', text, flags=re.IGNORECASE)

    # Remove Course Outcomes (CO1, CO2 etc)
    text = re.sub(r'CO\d+', '', text)

    # Remove page numbers
    text = re.sub(r'Page\s*\d+', '', text, flags=re.IGNORECASE)

    # Remove hours like 09 Hrs
    text = re.sub(r'\d+\s*Hrs?', '', text, flags=re.IGNORECASE)

    # Replace separators
    text = re.sub(r'[-:\n;]', ',', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove unwanted characters except comma
    text = re.sub(r'[^a-zA-Z0-9,\s]', ' ', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Split topics
    parts = [p.strip() for p in text.split(",")]

    clean_list = []

    for p in parts:
        # Remove long paragraph text
        if 3 < len(p) < 60:
            if not p.lower().startswith((
                "introduction",
                "overview",
                "course outcomes",
                "reference",
                "edition",
                "isbn"
            )):
                clean_list.append(p)

    # Remove duplicates
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)

# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Save output
df.to_excel("KIIT_Final_Cleaned.xlsx", index=False)

print("✅ UNIT headings completely removed. Clean topics extracted.")
