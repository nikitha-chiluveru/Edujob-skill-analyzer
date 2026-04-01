import fitz  # PyMuPDF
import pandas as pd
import re
import os
import glob

# 1. SETUP PATHS - This ensures Python finds your files
# Put your folder path here (e.g., r"C:/Users/RAKESH/Documents/INDUSTRY SCRAPING")
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)) 
os.chdir(FOLDER_PATH)

SOURCE_MAPPING = {
    "WEF": "WEF 2025",
    "NASSCOM": "NASSCOM 2025",
    "ISR": "ISR 2025",
    "DRAUP": "Draup–NASSCOM",
    "WHEEBOX": "ISR 2025"
}

def get_source_label(filename):
    fname = os.path.basename(filename).upper()
    for key, value in SOURCE_MAPPING.items():
        if key in fname: return value
    return "Industry Report 2025"

def auto_domain(text):
    s = text.lower()
    if any(x in s for x in ["ai", "learn", "neural", "vision", "nlp", "llm"]): return "Artificial Intelligence & Machine Learning"
    if any(x in s for x in ["data", "sql", "analyt", "spark", "hadoop", "bi"]): return "Data Science & Analytics"
    if any(x in s for x in ["cloud", "aws", "azure", "docker", "infra"]): return "Cloud Computing"
    if any(x in s for x in ["security", "cyber", "crypt", "protect", "threat"]): return "Cybersecurity"
    if any(x in s for x in ["develop", "soft", "code", "prog", "devops", "java", "python"]): return "Software Engineering"
    if any(x in s for x in ["think", "comm", "lead", "manage", "team", "problem"]): return "Soft & Employability Skills"
    return "Emerging Technologies"

def is_valid_industry_skill(text):
    words = text.split()
    # Skills are typically 2-6 words and start with a Capital letter
    if 2 <= len(words) <= 6 and text[0].isupper():
        garbage = ["page", "figure", "table", "http", "copyright", "source", "index", "report"]
        if not any(g in text.lower() for g in garbage):
            return True
    return False

def scrape_industry_data():
    # Find all PDFs in the folder
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print(f"❌ ERROR: No PDF files found in {FOLDER_PATH}")
        print("Please make sure your PDFs are in the SAME folder as this .py file.")
        return

    final_rows = []

    for pdf in pdf_files:
        source = get_source_label(pdf)
        print(f"🚀 Found File: {pdf} -> Labeling as: {source}")
        
        try:
            doc = fitz.open(pdf)
            for page in doc:
                # Analyze the page context for Demand Level
                page_text = page.get_text().lower()
                demand = "Moderate"
                if any(p in page_text for p in ["critical", "very high", "fastest", "top", "urgent"]):
                    demand = "Very High"
                elif any(p in page_text for p in ["high", "growing", "increasing", "priority", "rising"]):
                    demand = "High"

                # Extract text blocks
                blocks = page.get_text("blocks")
                for b in blocks:
                    block_content = b[4].strip()
                    lines = re.split(r'\n|•||▪|\*', block_content)
                    
                    for line in lines:
                        clean_line = line.strip()
                        if is_valid_industry_skill(clean_line):
                            # Final cleaning of non-alphanumeric start
                            skill_name = re.sub(r'^[^a-zA-Z0-9]+', '', clean_line)
                            
                            final_rows.append({
                                "Domain": auto_domain(skill_name),
                                "In-demand Industry Skill": skill_name,
                                "Demand Level": demand,
                                "Source": source
                            })
            doc.close()
        except Exception as e:
            print(f"⚠️ Error reading {pdf}: {e}")

    if final_rows:
        df = pd.DataFrame(final_rows)
        df = df.drop_duplicates(subset=["In-demand Industry Skill", "Source"])
        output_name = "Proper_Industry_Report_Data.csv"
        df[["Domain", "In-demand Industry Skill", "Demand Level", "Source"]].to_csv(output_name, index=False)
        print("\n" + "="*50)
        print(f"🏆 SUCCESS! File saved: {output_name}")
        print(f"📊 Total Unique Skills Scraped: {len(df)}")
        print("="*50)

if __name__ == "__main__":
    scrape_industry_data()
