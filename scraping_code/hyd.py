import pandas as pd
import re
import os

# 1. LOAD FILE
input_file = "iiit_syllabus.csv" 
output_file = "IIIT_HYD_FINAL_SUMMARY.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: {input_file} not found!")
    exit()

df = pd.read_csv(input_file)

def scrape_iit_pillars(text):
    if pd.isna(text) or str(text).strip() == "":
        return ""

    # A. KILL THE WASTE: Remove everything after "Reference Books", "Assessment", or "Teaching"
    # This deletes the long paragraphs at the end of the IIIT syllabus
    text = re.split(r'Reference Books|Teaching-Learning|Assessment methods|Note:', str(text), flags=re.IGNORECASE)[0]

    # B. STANDARDIZE BREAKS: Treat |, \n, bullet points (o), and colons as separators
    text = text.replace('|', ' , ').replace('\n', ' , ').replace(' o ', ' , ').replace(' • ', ' , ')
    
    # C. DELETE HEADERS: Remove "Unit 1", "Module I", etc.
    text = re.sub(r'\b(Unit|Module|Part|Section|Chapter)\s*[ivxl0-9l]+\b', ' , ', text, flags=re.IGNORECASE)

    # D. SPLIT into potential topics
    raw_segments = re.split(r'[,;:]', text)
    
    final_topics = []
    # Words to ignore for a "Summary" look
    noise = {"introduction", "overview", "basics", "fundamental", "fundamentals", "concepts", "concept", "theory", "brief"}

    for seg in raw_segments:
        # Clean numbering and special symbols at the start
        item = re.sub(r'^[\d\.\-\s\*\u2022\uf0b7o]+', '', seg.strip()).strip()
        
        # Split into words to filter noise and check length
        words = item.split()
        meaningful = [w for w in words if w.lower() not in noise]
        
        # --- THE SUMMARY RULE ---
        # Keep only segments that are 1 to 4 words long (Topic names)
        if 1 <= len(meaningful) <= 4:
            phrase = " ".join(meaningful).title().strip()
            # Remove trailing prepositions and garbage
            phrase = re.sub(r'\s(And|Of|The|To|With|For|In)$', '', phrase)
            phrase = re.sub(r'[^\w\s/]+$', '', phrase)
            
            if len(phrase) > 2 and phrase not in final_topics:
                final_topics.append(phrase)

    # Limit to top 15 most important topics per subject (Summary Style)
    if len(final_topics) > 15:
        final_topics = final_topics[:12]

    return ", ".join(final_topics)

# 2. APPLY CLEANING
df["Topics Covered"] = df["Topics Covered"].apply(scrape_iit_pillars)

# 3. FORMATTING (Exact match to your sample style)
df["Subject"] = df["Subject"].str.upper().str.strip()
df["College Name"] = "IIIT Hyderabad"

# 4. SAVE
df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Generated '{output_file}' with summarized IIIT topics.")
