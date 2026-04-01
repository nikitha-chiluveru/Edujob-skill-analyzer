import pandas as pd
import re
import os

# 1. USING THE EXACT FILENAMES FROM YOUR FOLDER LIST
input_file = "SRM_AP_Detailed_Syllabus.xlsx" 
output_file = "SRM_AP_SUMMARY_FINAL.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: Could not find '{input_file}' in your directory.")
    print("Please make sure you are running the script in the same folder as the Excel file.")
    exit()

# Load the Excel file directly
df = pd.read_excel(input_file)

def extract_neat_pillars(text):
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)
    
    # A. REMOVE SRM NARRATIVE ("We will examine...", "tip of the iceberg")
    # This deletes the wordy sentences that make the syllabus look messy.
    text = re.sub(r'We will (examine|understand|use|learn|introduce|discuss|explore|study).*?(\.|$)', ' , ', text, flags=re.IGNORECASE)
    text = re.sub(r'tip of the iceberg|possible due to chance|carefully supervised', '', text, flags=re.IGNORECASE)

    # B. STANDARDIZE: Convert Units, Newlines, and Colons into commas
    text = text.replace('\n', ' , ').replace(':', ' , ').replace(';', ' , ')
    text = re.sub(r'\bUNIT\s+[IVXL0-9]+\b[:\-]?\s*', ' , ', text, flags=re.IGNORECASE)

    # C. FILTER WASTE: Academic filler words
    waste = {
        "introduction", "overview", "basics", "fundamental", "fundamentals", 
        "concepts", "concept", "theory", "study", "discussion", "principles",
        "understanding", "steps", "examples", "sample", "programs", "creating", 
        "running", "simple", "complex", "applications", "approach"
    }

    # D. SPLIT & EXTRACT PILLARS
    segments = re.split(r'[,]', text)
    final_topics = []

    for seg in segments:
        # Clean numbering, bullets, and special symbols
        item = re.sub(r'^[\d\.\-\s\*\u2022\uf0b7]+', '', seg.strip()).strip()
        
        words = item.split()
        # Filter generic words
        meaningful = [w for w in words if w.lower() not in waste]
        
        # --- THE SUMMARY RULE (1-4 words) ---
        if 1 <= len(meaningful) <= 4:
            phrase = " ".join(meaningful).title().strip()
            # Clean trailing prepositions
            phrase = re.sub(r'\s(And|Of|The|To|With|For|In|By)$', '', phrase)
            
            if len(phrase) > 3 and phrase not in final_topics:
                final_topics.append(phrase)

    # E. LIMIT: Top 12 pillars for a neat summary visual
    if len(final_topics) > 15:
        final_topics = final_topics[:12]

    return ", ".join(final_topics)

# 2. APPLY TO ALL
# Note: Excel columns often have spaces; this finds the right one
target_col = "Topics Covered" if "Topics Covered" in df.columns else df.columns[-1]
df["Topics Covered"] = df[target_col].apply(extract_neat_pillars)

# 3. FORMATTING (Uppercase Subject and College Name)
df["Subject"] = df["Subject"].str.upper().str.strip()
df["College Name"] = "SRM UNIVERSITY AP"

# 4. SAVE
# Save as CSV to match your desired format
df[["College Name", "Subject", "Topics Covered"]].to_csv(output_file, index=False)

print(f"✅ SUCCESS! Generated '{output_file}' with neat, technical summaries.")
       
