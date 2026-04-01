import pandas as pd
import re
import os

# 1. SETUP FILENAME (Matches the .xlsx file found in your folder list)
input_file = "IIT_Madras_Detailed_Syllabus.xlsx"
output_file = "IIT_Madras_SUMMARY_FINAL.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: {input_file} not found in folder!")
    exit()

# Load the Excel file directly
try:
    # Reading Sheet1 as specified in your previous requirements
    df = pd.read_excel(input_file, sheet_name=0) 
except Exception as e:
    print(f"❌ Error loading Excel: {e}")
    exit()

# 2. PROCESSING LOGIC (The IIT Bombay Cleaning Logic)
def clean_subject(name):
    """Removes Course Codes and cleans Title"""
    if pd.isna(name): return ""
    text = str(name)
    # Remove IITM Course Codes (e.g., CS1100)
    text = re.sub(r'\b[A-Z]{2}\s*\d{4}\b', '', text)
    # Split at delimiters (dashes/colons)
    for delim in ["-", "−", ":"]:
        if delim in text:
            text = text.split(delim)[0]
            break
    return text.strip().upper()

def extract_pillars(text):
    """Strips narrative and extracts short technical phrases (1-4 words)"""
    if pd.isna(text) or str(text).strip() == "":
        return ""
    
    # Standardize separators
    text = str(text).replace('|', ' , ').replace('\n', ' , ').replace(':', ' , ').replace(';', ' , ')
    
    # Words to ignore for a clean look
    rejects = {"introduction", "overview", "basics", "fundamental", "concepts", "theory", "various", "foundational", "module", "lectures"}
    
    segments = re.split(r'[,]', text)
    final_topics = []
    
    for seg in segments:
        # Clean bullets/numbers
        item = re.sub(r'^[\d\.\-\s\*\u2022]+', '', seg.strip()).strip()
        words = item.split()
        meaningful = [w for w in words if w.lower() not in rejects]
        
        # Only keep short, punchy technical phrases
        if 1 <= len(meaningful) <= 4:
            phrase = " ".join(meaningful).title().strip()
            # Clean trailing prepositions
            phrase = re.sub(r'\s(And|Of|The|To|With|For|In|By)$', '', phrase)
            if len(phrase) > 3 and phrase not in final_topics:
                final_topics.append(phrase)
                
    return ", ".join(final_topics[:12])

# 3. APPLY AND SAVE
# IIT Madras Excel Column structure: index 2 is Name, index 3 is Topics
df["Subject"] = df.iloc[:, 2].apply(clean_subject)
df["Topics Covered"] = df.iloc[:, 3].apply(extract_pillars)
df["College Name"] = "IIT MADRAS"

final_df = df[["College Name", "Subject", "Topics Covered"]]
final_df = final_df[final_df["Subject"] != ""]

# Save Final Result
final_df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Processed '{input_file}'")
print(f"✅ Final CSV saved as '{output_file}'")
print(final_df.head())
