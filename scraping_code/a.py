import pandas as pd
import re
import os

# 1. LOAD FILE
input_file = "amity_syllabus.csv" 
output_file = "AMITY_FINAL_STRUCTURED.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: {input_file} not found! Ensure it is named 'amity_syllabus.csv'")
    exit()

df = pd.read_csv(input_file)

# Words to remove to keep the output clean like your sample
WASTE_WORDS = {
    "introduction", "overview", "basics", "basic", "concept", "concepts", 
    "fundamentals", "principles", "advanced", "study", "understanding", 
    "theory", "analysis", "features", "history", "evolution"
}

def extract_summary_topics(text):
    if pd.isna(text) or str(text).strip() == "":
        return "Technical Core"

    # Standardize breaks: Amity uses | and \n
    text = str(text).replace('|', ' , ').replace('\n', ' , ')
    
    # Remove Module/Unit/Part headers (e.g., Module I, Unit 1)
    text = re.sub(r'\b(module|unit|lecture|part|chapter|section)\s*(i{1,5}|v|x|l|\d+)\s*:?', ' , ', text, flags=re.IGNORECASE)

    # Split by comma, semicolon, or period
    segments = re.split(r'[,;.]', text)
    
    final_topics = []
    for seg in segments:
        # Clean numbering (1.1, a., etc)
        item = re.sub(r'^[\d\.\-\s]+', '', seg.strip()).strip()
        
        # Split into words to filter out waste
        words = item.split()
        clean_words = [w for w in words if w.lower() not in WASTE_WORDS]
        
        # --- THE SUMMARY RULE ---
        # Actual topics in your sample are usually 1-3 words.
        # We take the first 3 meaningful words of any segment.
        phrase = " ".join(clean_words[:3]).title().strip()
        
        if len(phrase) > 2 and phrase not in final_topics:
            # Remove trailing 'And', 'Of'
            phrase = re.sub(r'\s(And|Of|The|To|With|For)$', '', phrase)
            final_topics.append(phrase)

    # Match your manual sample: usually 10-15 key topics per subject
    if len(final_topics) > 15:
        final_topics = final_topics[:12]

    return ", ".join(final_topics)

# 2. APPLY
df["Topics Covered"] = df["Topics Covered"].apply(extract_summary_topics)

# 3. FORMATTING (Exact match to your sample picture)
df["Subject"] = df["Subject"].str.upper().str.strip()
df["College Name"] = "Amity University"

# 4. SAVE
df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Final file '{output_file}' generated. Every subject now has topics.")
