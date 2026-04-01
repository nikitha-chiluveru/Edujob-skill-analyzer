import pandas as pd
import re
import os

# 1. SETUP FILENAME (Using the exact name from your folder)
input_file = "Vellore_Syllabus_Complete.xlsx" 
output_file = "VIT_SUMMARY_FINAL.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: Could not find '{input_file}' in the folder.")
    print("Please ensure the file name matches exactly.")
    exit()

# Load the Excel file directly
# Note: You may need 'pip install openpyxl' if not already installed
df = pd.read_excel(input_file)

def clean_subject_name(name):
    """Removes VIT Course Codes (e.g., BMAT205L) to leave only the Title"""
    if pd.isna(name): return ""
    # Regex to remove 4 letters followed by 3 numbers and an optional L/P
    cleaned = re.sub(r'^[A-Z]{4}\d{3}[L|P]?\s*,?\s*', '', str(name))
    return cleaned.strip().upper()

def extract_vit_pillars(text):
    """Strips Module labels and filters for high-value technical topics"""
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)
    
    # A. STANDARDIZE: Replace | and newlines with commas
    text = text.replace('|', ' , ').replace('\n', ' , ')
    
    # B. STRIP LABELS: Remove "Mod 1:", "Mod 2:", etc.
    text = re.sub(r'\bMod\s*\d+\s*[:\-]?\s*', ' , ', text, flags=re.IGNORECASE)
    
    # C. REMOVE GENERIC TOPICS: VIT always has 'Contemporary Issues' at the end
    text = re.sub(r'Contemporary Issues', '', text, flags=re.IGNORECASE)

    # D. REJECT LIST: Generic words that clutter the 'Pillar' look
    rejects = {
        "introduction", "overview", "basics", "fundamental", "fundamentals", 
        "concepts", "concept", "theory", "study", "discussion", "principles",
        "understanding", "towards", "brief", "simple", "various", "context"
    }

    segments = re.split(r'[,]', text)
    final_topics = []

    for seg in segments:
        # Clean numbering, dashes, and extra spaces
        item = re.sub(r'^[\d\.\-\s\*\u2022]+', '', seg.strip()).strip()
        
        words = item.split()
        # Keep only segments that are 1-4 words (Matching your image style)
        clean_words = [w for w in words if w.lower() not in rejects]
        
        if 1 <= len(clean_words) <= 4:
            phrase = " ".join(clean_words).title().strip()
            # Clean trailing prepositions (Of, And, To, etc.)
            phrase = re.sub(r'\s(And|Of|The|To|With|For|In)$', '', phrase)
            
            if len(phrase) > 3 and phrase not in final_topics:
                final_topics.append(phrase)

    # E. LIMIT: Max 12 pillars per subject for that clean visual look
    return ", ".join(final_topics[:12])

# 2. PROCESS DATA
# Detect correct column names from your Excel
subj_col = "Subject Name" if "Subject Name" in df.columns else "Subject"
topics_col = "Topics Covered" if "Topics Covered" in df.columns else df.columns[-1]

df["Subject"] = df[subj_col].apply(clean_subject_name)
df["Topics Covered"] = df[topics_col].apply(extract_vit_pillars)
df["College Name"] = "VIT" 

# 3. FINAL FORMAT & SAVE
# Outputting exactly the 3 columns shown in your reference image
final_df = df[["College Name", "Subject", "Topics Covered"]]
final_df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Generated '{output_file}'")
print(final_df.head())
