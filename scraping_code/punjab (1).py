import pandas as pd
import re

df = pd.read_excel("Punjab_Syllabus_Output.xlsx")

def clean_topics(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove course codes
    text = re.sub(r'UE\d+\w*', '', text)

    # Remove textbook and lab sections only (strict)
    text = re.sub(r'Text Book.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Reference Book.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Tools.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Lab.*', '', text, flags=re.IGNORECASE)

    # Replace separators
    text = re.sub(r'[:;\n\-–\.]', ',', text)

    # Clean spacing
    text = re.sub(r'\s+', ' ', text)

    parts = [p.strip() for p in text.split(",")]

    clean_list = []

    for p in parts:
        if p == "":
            continue

        # Remove only very long sentences (descriptions)
        if len(p.split()) > 20:
            continue

        clean_list.append(p)

    # Remove duplicates but keep order
    clean_list = list(dict.fromkeys(clean_list))

    return ", ".join(clean_list)


df["Topics Covered"] = df["Topics Covered"].apply(clean_topics)

df = df[df["Topics Covered"] != ""]

df.to_excel("Punjab_Cleaned_Final.xlsx", index=False)

print("✅ Punjab syllabus cleaned properly without losing DBMS topics!")
