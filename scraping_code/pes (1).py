import pandas as pd
import re

# Load the file
df = pd.read_excel("PES_Syllabus_Output.xlsx")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove UNIT patterns (UNIT I, UNIT II, etc.)
    text = re.sub(r'UNIT\s*[-–:]?\s*(\d+|I+|V|X+)', '', text, flags=re.IGNORECASE)

    # Remove hours like 09 Hrs
    text = re.sub(r'\d+\s*Hrs?', '', text, flags=re.IGNORECASE)

    # Replace separators with comma
    text = re.sub(r'[-:]', ',', text)
    text = text.replace("\n", ",")
    text = text.replace(";", ",")

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
        # Keep only proper length topics (avoid long sentences)
        if 3 < len(p) < 70:
            # Remove weak starting words
            if not p.lower().startswith((
                "introduction",
                "overview",
                "applications",
                "case study",
                "case studies",
                "example",
                "examples"
            )):
                clean_list.append(p)

    # Remove duplicates while preserving order
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)

# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Save cleaned file
df.to_excel("PES_Final_Cleaned.xlsx", index=False)

print("✅ PES syllabus cleaned successfully.")
