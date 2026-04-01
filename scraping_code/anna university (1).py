import pandas as pd
import re

# Load file
df = pd.read_excel("Anna_University.xlsx")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove hour patterns like 9+3, 6+12
    text = re.sub(r'\d+\s*\+\s*\d+', '', text)

    # Remove UNIT headings
    text = re.sub(r'UNIT\s*[-–]?\s*[IVXLC\d]+', '', text, flags=re.IGNORECASE)

    # Remove PERIODS sections
    text = re.sub(r'\d+\s*PERIODS?.*', '', text, flags=re.IGNORECASE)

    # Remove years
    text = re.sub(r'\b\d{4}\b', '', text)

    # Remove brackets content
    text = re.sub(r'\(.*?\)', '', text)

    # Replace separators with comma
    text = re.sub(r'[:;\n\-–]', ',', text)

    # Clean extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    parts = [p.strip() for p in text.split(",")]

    clean_list = []

    for p in parts:

        # Skip very small fragments
        if len(p) < 4:
            continue

        word_count = len(p.split())

        # Remove full sentences (too long)
        if word_count > 12:
            continue

        # Remove phrases that start with action words (likely description)
        if p.lower().startswith(("introduction", "discussion", "writing", "reading", "speaking", "making", "working", "study of", "implementation of")):
            continue

        # Remove generic explanation words
        unwanted = [
            "importance",
            "benefits",
            "need for",
            "case study",
            "example",
            "definition",
            "overview",
            "advantages",
            "limitations"
        ]

        if any(word in p.lower() for word in unwanted):
            continue

        clean_list.append(p.strip())

    # Remove duplicates
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)


# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove empty rows
df = df[df["Topics Covered"] != ""]

# Save
df.to_excel("Anna_University_Pure_Topics_Final.xlsx", index=False)

print("✅ Anna University cleaned correctly.")
