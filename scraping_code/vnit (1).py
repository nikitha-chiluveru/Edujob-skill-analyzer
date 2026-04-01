import pandas as pd
import re

# Load file
file_path = "VNIT_Nagpur_Full_Syllabus.xlsx"
df = pd.read_excel(file_path)

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # 1️⃣ Remove page numbers
    text = re.sub(r'Page\s+\d+\s+of\s+\d+.*', '', text)

    # 2️⃣ Remove course objectives/outcomes blocks
    text = re.sub(r'Course Objectives.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Course Outcomes.*', '', text, flags=re.IGNORECASE)

    # 3️⃣ Remove textbook / reference lines
    text = re.sub(r'Reference.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Text\s*/?\s*References?.*', '', text, flags=re.IGNORECASE)

    # 4️⃣ Remove author names ending with publishers
    text = re.sub(r'.*(Wiley|McGraw|Pearson|Press|PHI|Elsevier).*', '', text)

    # 5️⃣ Replace separators with comma
    text = re.sub(r'[:;\n\-–]', ',', text)

    # 6️⃣ Remove extra symbols
    text = re.sub(r'[^a-zA-Z0-9,\s/]', '', text)

    # 7️⃣ Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # 8️⃣ Split into possible topics
    parts = text.split(",")

    clean_parts = []

    for p in parts:
        p = p.strip()

        # Skip very small junk
        if len(p) < 3:
            continue

        # Skip very long descriptive sentences
        if len(p.split()) > 18:
            continue

        # Skip random incomplete phrases
        if p.lower().startswith(("page", "using", "create", "www", "refer")):
            continue

        clean_parts.append(p)

    # Remove duplicates while keeping order
    clean_parts = list(dict.fromkeys(clean_parts))

    return ", ".join(clean_parts)


# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove fully empty rows
df = df[df["Topics Covered"] != ""]

# Save cleaned file
df.to_excel("VNIT_Cleaned_Topics_Final.xlsx", index=False)

print("✅ VNIT topics cleaned correctly without losing important topics!")
