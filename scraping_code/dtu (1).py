import pandas as pd
import re

# Load file
df = pd.read_csv("dtu syllabus.csv")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove everything like:
    # "Contents Contact Hours"
    # "Contact Hours"
    # "Contact Hour"
    text = re.sub(r'Contents?\s*Contact\s*Hours?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Contact\s*Hours?', '', text, flags=re.IGNORECASE)

    # Remove UNIT I, UNIT II etc
    text = re.sub(r'UNIT\s*[IVXLC]+\b', '', text, flags=re.IGNORECASE)

    # Remove S. No, No.
    text = re.sub(r'\bS\.?\s*No\.?\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bNo\.?\b', '', text, flags=re.IGNORECASE)

    # Remove standalone numbers like 6,7,8,10
    text = re.sub(r'\b\d+\b', '', text)

    # Remove ISBN lines
    text = re.sub(r'ISBN[\w\s\-–]*', '', text, flags=re.IGNORECASE)

    # Replace separators with comma
    text = re.sub(r'[:;\n|]', ',', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Split into topics
    topics = [t.strip() for t in text.split(",")]

    # Keep meaningful topics only
    clean_list = []
    for t in topics:
        if len(t) > 4:
            clean_list.append(t)

    # Remove duplicates
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)


# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove empty rows
df = df[df["Topics Covered"] != ""]

# Save new file
df.to_csv("DTU_Final_Cleaned.csv", index=False)

print("✅ Contact Hours completely removed.")
