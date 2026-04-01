import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("🔄 Loading datasets...")

# -----------------------------
# STEP 1: Load Files
# -----------------------------

college_df = pd.read_csv("clustered_output.csv")
industry_df = pd.read_csv("processed_industry_skills.csv")

# Remove hidden spaces in column names
college_df.columns = college_df.columns.str.strip()
industry_df.columns = industry_df.columns.str.strip()

print("✅ Files loaded successfully")

# -----------------------------
# STEP 2: Extract & Split College Topics
# -----------------------------

college_text = college_df["Topics Covered"].dropna().tolist()

college_skills = []

for text in college_text:
    parts = str(text).split(",")
    for part in parts:
        cleaned = part.strip().lower()
        if len(cleaned) > 2:
            college_skills.append(cleaned)

college_skills = list(set(college_skills))

print("🎓 Total College Skills Extracted:", len(college_skills))

# -----------------------------
# STEP 3: Load SBERT Model
# -----------------------------

print("🔄 Loading SBERT model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("🔄 Creating embeddings for college skills...")
college_embeddings = model.encode(college_skills)

threshold = 0.80

domain_results = []
matched_records = []
missing_records = []

print("🔄 Starting Semantic Comparison...")

# -----------------------------
# STEP 4: Domain-wise Comparison
# -----------------------------

for domain in industry_df["Domain"].unique():

    print(f"\n📌 Processing Domain: {domain}")

    domain_df = industry_df[industry_df["Domain"] == domain]

    industry_skills = domain_df["clean_skill"].dropna().unique().tolist()

    if len(industry_skills) == 0:
        continue

    industry_embeddings = model.encode(industry_skills)

    similarity_matrix = cosine_similarity(college_embeddings, industry_embeddings)

    matched_skills = set()

    for i in range(len(college_skills)):
        similarities = similarity_matrix[i]
        max_score = np.max(similarities)

        if max_score >= threshold:
            best_match_index = np.argmax(similarities)
            matched_skills.add(industry_skills[best_match_index])

    total_skills = len(industry_skills)
    matched_count = len(matched_skills)
    missing_skills = list(set(industry_skills) - matched_skills)
    missing_count = len(missing_skills)

    coverage = (matched_count / total_skills) * 100 if total_skills != 0 else 0

    domain_results.append({
        "Domain": domain,
        "Total Industry Skills": total_skills,
        "Matched Skills": matched_count,
        "Missing Skills": missing_count,
        "Coverage %": round(coverage, 2)
    })

    for skill in matched_skills:
        matched_records.append({
            "Domain": domain,
            "Matched Skill": skill
        })

    for skill in missing_skills:
        missing_records.append({
            "Domain": domain,
            "Missing Skill": skill
        })

# -----------------------------
# STEP 5: Save Reports
# -----------------------------

domain_report = pd.DataFrame(domain_results)
domain_report = domain_report.sort_values(by="Coverage %", ascending=False)

matched_df = pd.DataFrame(matched_records)
missing_df = pd.DataFrame(missing_records)

print("\n🔥 ===== SEMANTIC DOMAIN GAP REPORT ===== 🔥")
print(domain_report)

domain_report.to_csv("semantic_domain_gap_report.csv", index=False)
matched_df.to_csv("semantic_matched_skills.csv", index=False)
missing_df.to_csv("semantic_missing_skills.csv", index=False)

print("\n✅ Reports generated successfully!")