import os
import PyPDF2
import docx
import re
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["skillgap_database"]
industry_collection = db["industry_skills"]

SIMILARITY_THRESHOLD = 0.60


# -----------------------------
# Extract Resume Text
# -----------------------------
def extract_text(file):

    text = ""

    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = " ".join([para.text for para in doc.paragraphs])

    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")

    return text.lower()


# -----------------------------
# Extract Skills from Resume
# -----------------------------
def extract_resume_skills(resume_text):

    words = re.findall(r'\b[a-zA-Z]+\b', resume_text)

    unique_words = list(set(words))

    return unique_words


# -----------------------------
# Compare Resume with Industry
# -----------------------------
def analyze_resume(resume_text):

    industry_data = list(industry_collection.find({}, {"_id": 0}))

    resume_skills = extract_resume_skills(resume_text)

    domain_results = {}

    resume_embeddings = model.encode(resume_skills)

    for item in industry_data:

        domain = item["domain"]
        skill = item["skill"].lower()

        if domain not in domain_results:
            domain_results[domain] = {
                "total": 0,
                "matched": [],
                "missing": []
            }

        domain_results[domain]["total"] += 1

        skill_embedding = model.encode([skill])

        similarities = cosine_similarity(resume_embeddings, skill_embedding)

        max_similarity = np.max(similarities)

        if max_similarity >= SIMILARITY_THRESHOLD:
            domain_results[domain]["matched"].append(skill)
        else:
            domain_results[domain]["missing"].append(skill)

    # Calculate suitability
    for domain in domain_results:

        total = domain_results[domain]["total"]
        matched = len(domain_results[domain]["matched"])

        coverage = round((matched / total) * 100, 2)

        domain_results[domain]["suitability"] = coverage

    return domain_results


# -----------------------------
# KNN Domain Recommendation
# -----------------------------
def find_nearest_domains(resume_text):

    industry_data = list(industry_collection.find({}, {"_id": 0}))

    domains = []
    skills = []

    for item in industry_data:
        domains.append(item["domain"])
        skills.append(item["skill"].lower())

    # Convert skills into embeddings
    skill_embeddings = model.encode(skills)

    # Convert resume text into embedding
    resume_embedding = model.encode([resume_text])

    # KNN model
    knn = NearestNeighbors(n_neighbors=5, metric="cosine")

    knn.fit(skill_embeddings)

    distances, indices = knn.kneighbors(resume_embedding)

    nearest_domains = []

    for idx in indices[0]:
        nearest_domains.append(domains[idx])

    # remove duplicates
    nearest_domains = list(set(nearest_domains))

    return nearest_domains