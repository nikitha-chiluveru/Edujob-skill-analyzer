import pandas as pd
import re

# Load file
file_path = "Thiagarajar_Syllabus_Final.xlsx"
df = pd.read_excel(file_path)

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # 1️⃣ Remove numbers like "1 |", "2 |"
    text = re.sub(r'\b\d+\b', '', text)

    # 2️⃣ Fix broken words (remove space inside words)
    text = re.sub(r'(\w)\s+(\w)', r'\1 \2', text)

    # 3️⃣ Replace | with comma
    text = text.replace("|", ",")

    # 4️⃣ Remove extra special characters
    text = re.sub(r'[^a-zA-Z0-9,\s\-/()]', '', text)

    # 5️⃣ Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # 6️⃣ Split into topics
    parts = text.split(",")

    clean_list = []

    for p in parts:
        p = p.strip()

        # Remove very short junk
        if len(p) < 3:
            continue

        # Remove very long descriptive sentences (likely junk)
        if len(p.split()) > 20:
            continue

        clean_list.append(p)

    # Remove duplicates while preserving order
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)


# Apply cleaning
df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

# Remove empty rows
df = df[df["Topics Covered"] != ""]

# Save cleaned file
df.to_excel("Thiagarajar_Cleaned_Final.xlsx", index=False)

print("✅ File cleaned successfully!")
