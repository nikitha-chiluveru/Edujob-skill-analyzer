import pandas as pd
import re

# Load file
df = pd.read_csv("mgit syllabus.csv", encoding="utf-8", engine="python")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Fix encoding garbage
    text = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")

    # Remove UNIT labels
    text = re.sub(r'UNIT\s*[-–]?\s*[IVX0-9]+:?','', text, flags=re.IGNORECASE)

    # Remove MR- B.Tech junk lines
    text = re.sub(r'MR-.*?Hyderabad','', text, flags=re.IGNORECASE)

    # Remove repeated MGIT junk
    text = re.sub(r'MGIT\s*\(.*?\)','', text, flags=re.IGNORECASE)

    # Remove syllabus warning rows
    if "Syllabus topics not clearly structured" in text:
        return ""

    # Remove standalone numbers
    text = re.sub(r'\b\d+\b', '', text)

    # Replace weird separators
    text = text.replace("|", ",")
    text = text.replace("â€“", "-")
    text = text.replace("â€™", "'")

    # Remove multiple commas
    text = re.sub(r',+', ',', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Clean edges
    text = text.strip(" ,")

    return text


# Apply cleaning ONLY to Topics Covered column
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove completely empty topic rows
df = df[df["Topics Covered"] != ""]

# Save file
df.to_csv("mgit_cleaned_proper.csv", index=False)

print("✅ MGIT topics cleaned properly!")
