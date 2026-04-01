import pandas as pd
import re
import os

# 1. SETUP FILENAME (Using the exact name from your directory)
input_file = "IIT_Bombay_Syllabus.xlsx"
output_file = "IITB_SUMMARY_FINAL.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: {input_file} not found!")
    exit()

# Load the Excel file
try:
    df = pd.read_excel(input_file)
except Exception as e:
    print(f"❌ Error loading Excel: {e}")
    exit()

# 2. IMPROVED ROW MERGER (Fixes "Half-Half" Subject Names)
def merge_split_rows(data):
    new_rows = []
    i = 0
    while i < len(data):
        current_row = data.iloc[i].copy()
        
        # Check if next row is a continuation fragment
        while i + 1 < len(data):
            # Check the 'Subject' column of the next row (Index 1)
            next_subj = str(data.iloc[i+1, 1]).strip()
            
            # If the next row doesn't start with a Course Code (like CS 103), it's a continuation
            if not re.search(r'^[A-Z]{2}\s\d{3}', next_subj) and next_subj.lower() != 'nan':
                current_row.iloc[1] = f"{current_row.iloc[1]} {next_subj}"
                # Also merge the topics
                next_topics = str(data.iloc[i+1, 2]).strip()
                if next_topics.lower() != 'nan':
                    current_row.iloc[2] = f"{current_row.iloc[2]} | {next_topics}"
                i += 1
            else:
                break
        
        new_rows.append(current_row)
        i += 1
    return pd.DataFrame(new_rows)

df = merge_split_rows(df)

def clean_subject(name):
    """Cleans 'CS 103 Computing and Science − Description' -> 'COMPUTING AND SCIENCE'"""
    if pd.isna(name): return ""
    text = str(name)
    # Remove Course Codes
    text = re.sub(r'\b[A-Z]{2}\s*\d{3}\b', '', text)
    # Split at Dash
    for dash in ["−", "-", "—"]:
        if dash in text:
            text = text.split(dash)[0]
            break
    return text.strip().upper()

def extract_pillars(text):
    """Extracts topics and ensures it never returns a blank if text exists"""
    if pd.isna(text) or str(text).strip() == "" or str(text).lower() == 'nan':
        return "General Core Concepts"

    text = str(text).replace('|', ' , ').replace('\n', ' , ').replace(':', ' , ')
    
    # Narrative words to filter
    rejects = {"introduction", "overview", "basics", "fundamental", "concepts", "theory", "various", "foundational", "course", "connecting"}
    
    segments = re.split(r'[,]', text)
    final_topics = []
    
    for seg in segments:
        item = re.sub(r'^[\d\.\-\s\*\u2022]+', '', seg.strip()).strip()
        words = item.split()
        
        # Keep technical phrases (1-4 words)
        meaningful = [w for w in words if w.lower() not in rejects]
        
        if 1 <= len(meaningful) <= 5:
            phrase = " ".join(meaningful).title().strip()
            phrase = re.sub(r'\s(And|Of|The|To|With|For|In|By)$', '', phrase)
            if len(phrase) > 3 and phrase not in final_topics:
                final_topics.append(phrase)

    # FALLBACK: If filtering left us with nothing, just take the first few technical words
    if not final_topics:
        words = [w for w in text.split() if len(w) > 4 and w.lower() not in rejects]
        final_topics = [w.title() for w in words[:8]]

    return ", ".join(final_topics[:12])

# 3. APPLY AND SAVE
# We use position-based indexing (iloc) to avoid column name errors
df["Subject"] = df.iloc[:, 1].apply(clean_subject)
df["Topics Covered"] = df.iloc[:, 2].apply(extract_pillars)
df["College Name"] = "IIT BOMBAY"

final_df = df[["College Name", "Subject", "Topics Covered"]]
# Ensure we don't have rows with empty subjects
final_df = final_df[final_df["Subject"].str.len() > 2]

final_df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Generated '{output_file}'")
print(final_df.head())
