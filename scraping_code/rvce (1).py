import pandas as pd
import re

# Load your file
df = pd.read_excel("RVCE_Syllabus_Report.xlsx")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove UNIT headings
    text = re.sub(r'UNIT\s*[-–]?\s*(\d+|I+|V|X|L+)', '', text, flags=re.IGNORECASE)

    # Remove hours like 09 Hrs
    text = re.sub(r'\d+\s*Hrs?', '', text, flags=re.IGNORECASE)

    # Replace separators with comma
    text = re.sub(r'[-:\n;]', ',', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove unwanted characters
    text = re.sub(r'[^a-zA-Z0-9,\s]', ' ', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Split into parts
    parts = [p.strip() for p in text.split(",")]

    clean_list = []

    for p in parts:
        # Remove very long sentences (keep only small topic phrases)
        if 3 < len(p) < 60:
            # Remove phrases starting with weak words
            if not p.lower().startswith(("introduction", "overview", "applications", "case study", "case studies", "example", "examples")):
                clean_list.append(p)

    # Remove duplicates
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)

# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Save cleaned file
df.to_excel("RVCE_Final_Cleaned.xlsx", index=False)

print("✅ Cleaned successfully. Pure topic names extracted.")
