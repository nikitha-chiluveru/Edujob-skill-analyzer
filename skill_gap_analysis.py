import pandas as pd
import re

# -----------------------------
# STEP 1: Load Files
# -----------------------------

college_df = pd.read_csv("clustered_output.csv")
industry_df = pd.read_csv("processed_industry_skills.csv")

print("Files Loaded Successfully")

# -----------------------------
# STEP 2: Clean Text
# -----------------------------

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

college_df["clean_topics"] = college_df["Topics Covered"].apply(clean_text)

# -----------------------------
# STEP 3: Prepare Industry Skills
# -----------------------------

industry_df["clean_skill"] = industry_df["clean_skill"].str.lower()

industry_skills = industry_df["clean_skill"].unique()

# Demand Weights
def demand_weight(level):
    level = str(level).lower()
    if "very high" in level:
        return 3
    elif "high" in level:
        return 2
    else:
        return 1

industry_df["weight"] = industry_df["Demand Level"].apply(demand_weight)

# -----------------------------
# STEP 4: Skill Matching
# -----------------------------

matched_skills = set()

for text in college_df["clean_topics"]:
    for skill in industry_skills:
        if skill in text:
            matched_skills.add(skill)

matched_skills = list(matched_skills)

missing_skills = list(set(industry_skills) - set(matched_skills))

# -----------------------------
# STEP 5: Overall Coverage
# -----------------------------

total_skills = len(industry_skills)
coverage = (len(matched_skills) / total_skills) * 100

print("\n===== OVERALL COVERAGE =====")
print("Total Industry Skills:", total_skills)
print("Matched Skills:", len(matched_skills))
print("Coverage %:", round(coverage, 2))

# -----------------------------
# STEP 6: Domain-wise Coverage
# -----------------------------

domain_results = []

for domain in industry_df["Domain"].unique():

    domain_df = industry_df[industry_df["Domain"] == domain]
    domain_skills = domain_df["clean_skill"].unique()

    matched_domain = [skill for skill in domain_skills if skill in matched_skills]

    domain_coverage = (len(matched_domain) / len(domain_skills)) * 100

    domain_results.append({
        "Domain": domain,
        "Total Skills": len(domain_skills),
        "Matched Skills": len(matched_domain),
        "Coverage %": round(domain_coverage, 2)
    })

domain_report = pd.DataFrame(domain_results)

print("\n===== DOMAIN-WISE COVERAGE =====")
print(domain_report)

domain_report.to_csv("domain_gap_report.csv", index=False)

# -----------------------------
# STEP 7: Demand Weighted Coverage
# -----------------------------

total_weight = industry_df["weight"].sum()

matched_weight = industry_df[industry_df["clean_skill"].isin(matched_skills)]["weight"].sum()

weighted_coverage = (matched_weight / total_weight) * 100

print("\n===== DEMAND-WEIGHTED COVERAGE =====")
print("Weighted Coverage %:", round(weighted_coverage, 2))

# -----------------------------
# STEP 8: Save Skill Lists
# -----------------------------

pd.DataFrame(matched_skills, columns=["Matched_Skills"]).to_csv("matched_skills.csv", index=False)

pd.DataFrame(missing_skills, columns=["Missing_Skills"]).to_csv("missing_skills.csv", index=False)

print("\nReports Saved Successfully!")
print("domain_gap_report.csv generated")
print("matched_skills.csv generated")
print("missing_skills.csv generated")