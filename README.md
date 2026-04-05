# 🎯 EduJob Skill Analyzer

> An NLP-powered web application that quantifies the skill gap between engineering college curricula and IT industry requirements — at both the institutional and individual student level.

---

## 📌 About the Project

Fresh engineering graduates in India often enter the job market lacking skills that employers consider essential. EduJob Skill Analyzer addresses this by:

- 📊 Comparing college curriculum coverage against real industry skill demand (domain-wise)
- 📄 Analyzing individual student resumes to identify matched and missing skills
- 🎓 Recommending personalized Coursera learning resources for each missing skill
- 💡 Suggesting tiered project ideas (Beginner / Intermediate / Advanced) to build missing skills

---

## 🖥️ Demo

| Dashboard | Resume Analysis |
|-----------|----------------|
| Domain-wise skill coverage bar chart | Matched & missing skill tags with pie chart |

---

## 🏗️ System Architecture

```
Industry Data (NASSCOM)          College Syllabus (PDFs)
        ↓                                  ↓
  BeautifulSoup Scraper            PyPDF2 Extraction
        ↓                                  ↓
  Data Preprocessing ←————————————————————→
        ↓
  K-Means Clustering (k=10 domains)
        ↓
  ┌─────────────────────────────────┐
  │      Skill Matching Engine      │
  │  Keyword Matching + SBERT (θ=0.6) │
  └─────────────────────────────────┘
        ↓
  MongoDB (domain_comparison, matched_skills, missing_skills)
        ↓
  Streamlit Dashboard
  ├── 🏠 Dashboard (Plotly bar chart)
  ├── 📄 Resume Analysis (KNN recommendation + gap report)
  ├── 📚 Learning Resources (Coursera links)
  └── 💡 Project Ideas (Beginner / Intermediate / Advanced)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9+ |
| Frontend | Streamlit |
| NLP / ML | SBERT (sentence-transformers), scikit-learn |
| Database | MongoDB (pymongo) |
| Visualization | Plotly Express |
| Web Scraping | BeautifulSoup4, requests |
| Resume Parsing | PyPDF2, python-docx |
| Data Processing | pandas, NumPy |

---

## 🔍 Key Features

- **Dual Skill Matching** — Keyword-based matching for speed + SBERT semantic matching for accuracy (12–18% higher recall)
- **Demand-Weighted Scoring** — Skills weighted by industry demand level (Very High / High / Medium)
- **Resume Upload** — Supports PDF, DOCX, and TXT resume formats
- **KNN Domain Recommender** — Recommends best-fit tech domains based on resume skill profile (85% top-1 accuracy)
- **Learning Roadmap** — Direct Coursera course links for every identified missing skill
- **Project Ideas** — Tiered suggestions at Beginner, Intermediate, and Advanced levels

---

## 📂 Project Structure

```
Edujob-skill-analyzer/
│
├── streamlit_app.py              # Main Streamlit application
├── skill_gap_analysis.py         # Keyword-based skill matching pipeline
├── skill_gap_analysis_new.py     # SBERT semantic matching pipeline
├── clustering.py                 # K-Means clustering of syllabus topics
├── resume_model.py               # Resume text extraction + KNN recommender
├── insert_industry.py            # Industry skills preprocessing + MongoDB insert
│
├── upload_comparison_to_mongo.py # Upload domain comparison to MongoDB
├── upload_matched_skills.py      # Upload matched skills to MongoDB
├── upload_missing_skills.py      # Upload missing skills to MongoDB
│
├── scraping_code/                # BeautifulSoup scrapers for industry data
├── data/                         # Processed data files
├── raw_data/                     # Raw scraped and syllabus data
│
├── clustered_output.csv          # Syllabus topics after K-Means clustering
├── processed_industry_skills.csv # Cleaned industry skills dataset
├── domain_gap_report.csv         # Domain-wise coverage report
├── matched_skills.csv            # Skills found in curriculum
└── missing_skills.csv            # Skills absent from curriculum
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.9+
MongoDB running locally on port 27017
```

### Installation

```bash
# Clone the repository
git clone https://github.com/nikitha-chiluveru/Edujob-skill-analyzer.git
cd Edujob-skill-analyzer

# Install dependencies
pip install streamlit pymongo pandas numpy scikit-learn sentence-transformers plotly beautifulsoup4 requests PyPDF2 python-docx
```

### Running the Pipeline (First Time)

Run these scripts in order:

```bash
# Step 1: Scrape industry data
python scraping_code/scraper.py

# Step 2: Preprocess and insert industry skills into MongoDB
python insert_industry.py

# Step 3: Cluster syllabus topics by domain
python clustering.py

# Step 4: Run keyword-based skill gap analysis
python skill_gap_analysis.py

# Step 5: Run SBERT semantic skill gap analysis
python skill_gap_analysis_new.py

# Step 6: Upload results to MongoDB
python upload_comparison_to_mongo.py
python upload_matched_skills.py
python upload_missing_skills.py
```

### Launch the App

```bash
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Results

| Domain | Total Skills | Matched | Keyword Coverage | SBERT Coverage |
|--------|-------------|---------|-----------------|----------------|
| Data Science & ML | 85 | 52 | 61.2% | 74.1% |
| Web Development | 70 | 48 | 68.6% | 79.3% |
| Cloud Computing | 60 | 28 | 46.7% | 58.2% |
| Cybersecurity | 55 | 22 | 40.0% | 51.8% |
| Database Management | 45 | 38 | 84.4% | 88.9% |
| Soft Skills | 40 | 25 | 62.5% | 70.0% |

- SBERT semantic matching improves skill recall by **12–18%** over keyword matching
- KNN domain recommender achieves **85% top-1 accuracy** on test resumes

---

## 👩‍💻 Authors

- **Veda** — Department of Information Technology, Stanley College of Engineering and Technology for Women
- **Nikitha Chiluveru** — Department of Information Technology, Stanley College of Engineering and Technology for Women  
- **Yuktha** — Department of Information Technology, Stanley College of Engineering and Technology for Women
---

## 🙏 Acknowledgements

- [NASSCOM Future Skills](https://futureskills.nasscom.in/) — Industry skills data source
- [Sentence Transformers](https://www.sbert.net/) — SBERT model
- [Streamlit](https://streamlit.io/) — Web app framework
- Stanley College of Engineering and Technology for Women, Hyderabad

---

## 📝 License

This project is open-source and available for academic and educational use.
