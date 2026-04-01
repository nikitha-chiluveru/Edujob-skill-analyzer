import pandas as pd
import re
import os

# 1. LOAD FILE
input_file = "nit_trichy_fixed.csv" 
output_file = "NIT_TRICHY_SUMMARY_FINAL.csv"

if not os.path.exists(input_file):
    print(f"❌ Error: {input_file} not found!")
    exit()

df = pd.read_csv(input_file)

def extract_pure_technical_pillars(text):
    if pd.isna(text) or str(text).strip() == "":
        return "Technical Core"

    text = str(text)
    
    # A. FOCUS ON CONTENT: Ignore objectives and references
    if "Course Contents" in text:
        text = text.split("Course Contents", 1)[1]
    
    # Cut off references/assessments
    text = re.split(r'Reference Books|Assessment methods|Course Outcomes|Note:', text, flags=re.IGNORECASE)[0]

    # B. STANDARDIZE BREAKS: Handle pipes, newlines, and dashes
    text = text.replace('|', ' , ').replace('\n', ' , ').replace(' - ', ' , ').replace(' – ', ' , ')
    
    # C. DELETE BOILERPLATE: Remove "UNIT I", "MODULE 2", etc.
    text = re.sub(r'\b(UNIT|MODULE|PART|SECTION|SEMESTER|CODE)\s*[IVXL0-9]*\b', ' , ', text, flags=re.IGNORECASE)

    # D. SCRAPE TECHNICAL NOUNS
    segments = re.split(r'[,;.:\(\)]', text)
    final_topics = []
    
    # Garbage words to ignore for a clean summary
    garbage = {
        "introduction", "overview", "basics", "fundamental", "fundamentals", 
        "concept", "concepts", "theory", "study", "discussion", "principles",
        "understanding", "need", "features", "characteristics", "brief",
        "review", "evolution", "description", "definition", "representation"
    }
    
    # Leading words to strip from phrases
    leading_strip = {"to", "of", "and", "with", "from", "for", "in", "the", "using"}

    for seg in segments:
        # Clean specific symbols and bullets
        item = re.sub(r'^[\d\.\s\*\u2022\uf0b7\-o]+', '', seg.strip()).strip()
        words = item.split()
        
        # SUMMARY RULE: Reject sentences (> 5 words)
        if len(words) > 5 or len(words) == 0:
            continue
            
        # Strip generic words
        clean_words = [w for w in words if w.lower() not in garbage]
        
        # Trim leading/trailing prepositions (e.g., "To Logic" -> "Logic")
        while clean_words and clean_words[0].lower() in leading_strip:
            clean_words.pop(0)
        while clean_words and clean_words[-1].lower() in leading_strip:
            clean_words.pop(-1)
            
        # Target high-level topics (1-3 words)
        if 1 <= len(clean_words) <= 3:
            topic = " ".join(clean_words).title().strip()
            if len(topic) > 3 and topic not in final_topics:
                final_topics.append(topic)

    # E. LIMIT: Match your manual summary style (top 12 pillars)
    if len(final_topics) > 15:
        final_topics = final_topics[:12]
    
    return ", ".join(final_topics)

# 2. APPLY PROCESSING
df["Topics Covered"] = df["Topics Covered"].apply(extract_pure_technical_pillars)

# 3. FINAL FORMATTING (Uppercase Subject & College)
df["Subject"] = df["Subject"].str.upper().str.strip()
df["College Name"] = "NIT TIRUCHIRAPPALLI"

# 4. SAVE
df.to_csv(output_file, index=False)

print(f"✅ SUCCESS! Generated '{output_file}' with summarized NIT topics.")
