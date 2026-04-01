import streamlit as st
from pymongo import MongoClient
from resume_model import extract_text, analyze_resume, find_nearest_domains
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EduJob Skill Analyzer", layout="wide")

# ===============================
# DARK UI
# ===============================
st.markdown("""
<style>
.stApp { background-color: #0f172a; color: white; }

section[data-testid="stSidebar"] { background-color: #020617; }
section[data-testid="stSidebar"] * { color: white; }

h1,h2,h3,h4,h5,h6,p { color: white !important; }

.tag-green {
    background:#166534;
    padding:8px 14px;
    border-radius:20px;
    margin:5px;
    display:inline-block;
}

.tag-red {
    background:#7f1d1d;
    padding:8px 14px;
    border-radius:20px;
    margin:5px;
    display:inline-block;
}

.card {
    background:#1e293b;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("📊 EduJob")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📄 Resume Analysis", "📚 Learning Resources", "💡 Project Ideas"]
)

st.title("🎯 EduJob Skill Analyzer")

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["skill_gap_project"]

# ===============================
# DASHBOARD
# ===============================
if menu == "🏠 Dashboard":

    col1, col2 = st.columns([3, 1])

    # LEFT SIDE (CHART)
    with col1:
        st.header("🎓 College vs Industry Skill Gap")

        data = list(db["domain_comparison"].find())

        if data:
            df = pd.DataFrame(data).drop(columns=["_id"])

            fig = px.bar(
                df.sort_values(by="Coverage %"),
                x="Coverage %",
                y="Domain",
                orientation="h",
                color="Coverage %",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

    # RIGHT SIDE (INFO PANEL)
    with col2:
        st.markdown("""
        <div style="margin-top:-60px; background:#1e293b; padding:20px; border-radius:10px;">

        <h3>📌 About EduJob Skill Analyzer</h3>

        <p>
        EduJob Skill Analyzer identifies skill gaps between academic curriculum 
        and industry requirements, performs resume analysis, recommends domains, 
        and provides learning resources and project ideas to bridge skill gaps.
        </p>

        <h4>📊 Data Sources</h4>
        <ul>
            <li>College Syllabus</li>
            <li>NASSCOM Reports</li>
        </ul>

        <h4>⚙️ Tech Stack</h4>
        <ul>
            <li>Python</li>
            <li>SBERT (NLP)</li>
            <li>MongoDB</li>
            <li>Streamlit</li>
            <li>Plotly</li>
            <li>KNN Algorithm</li>
            <li>BeautifulSoup (Web Scraping)</li>
        </ul>

        <p><b>👩‍💻 Created by:</b> Veda, Nikitha, Yuktha</p>

        </div>
        """, unsafe_allow_html=True)

# ===============================
# RESUME ANALYSIS
# ===============================
if menu == "📄 Resume Analysis":

    st.header("👤 Resume Analysis")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if uploaded_file:
        st.session_state["file"] = uploaded_file

    if "file" in st.session_state:

        resume_text = extract_text(st.session_state["file"])

        nearest_domains = find_nearest_domains(resume_text)

        st.subheader("🎯 Recommended Domains")

        st.markdown(f"""
        <div style="display:flex;flex-wrap:wrap;">
        {"".join([f"<div class='card'>{d}</div>" for d in nearest_domains])}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        results = analyze_resume(resume_text)
        st.session_state["results"] = results

        for domain, data in results.items():

            st.subheader(domain)

            matched = len(data["matched"])
            missing = len(data["missing"])

            pie_df = pd.DataFrame({
                "Type": ["Matched", "Missing"],
                "Count": [matched, missing]
            })

            fig = px.pie(
                pie_df,
                names="Type",
                values="Count",
                hole=0.5,
                template="plotly_dark",
                color_discrete_map={
                    "Matched": "#22c55e",
                    "Missing": "#ef4444"
                }
            )

            st.plotly_chart(fig, use_container_width=True, key=f"pie_{domain}")

            st.markdown("### 🟢 Matched Skills")
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;">
            {"".join([f"<div class='tag-green'>{s}</div>" for s in data["matched"]])}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🔴 Missing Skills")
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;">
            {"".join([f"<div class='tag-red'>{s}</div>" for s in data["missing"]])}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

# ===============================
# LEARNING RESOURCES
# ===============================
if menu == "📚 Learning Resources":

    st.header("📚 Learning Resources")

    if "results" not in st.session_state:
        st.warning("Upload resume first")
    else:

        for domain, data in st.session_state["results"].items():

            st.subheader(domain)

            for skill in data["missing"]:

                link = f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}"

                st.markdown(f"""
                <div class="card">
                📘 <b>{skill}</b><br>
                <a href="{link}" target="_blank">🎓 Learn Course</a>
                </div>
                """, unsafe_allow_html=True)

# ===============================
# PROJECT IDEAS
# ===============================
if menu == "💡 Project Ideas":

    st.header("💡 Smart Project Roadmap")

    if "results" not in st.session_state:
        st.warning("Upload resume first")
    else:

        results = st.session_state["results"]

        exclude_domains = [
            "Soft & Employability Skills",
            "Aptitude",
            "Communication Skills"
        ]

        filtered_domains = {
            d: v for d, v in results.items()
            if d not in exclude_domains and v["suitability"] >= 20
        }

        sorted_domains = sorted(
            filtered_domains.items(),
            key=lambda x: x[1]["suitability"],
            reverse=True
        )

        shown = 0

        for domain, data in sorted_domains:

            if shown >= 2:
                break

            st.subheader(f"📌 {domain} ({data['suitability']}%)")

            missing_skills = data["missing"][:5]

            if missing_skills:

                tab1, tab2, tab3 = st.tabs(["Beginner", "Intermediate", "Advanced"])

                def card(title, skill, level, desc):
                    return f"""
                    <div style="background:#1e293b;padding:15px;border-radius:10px;margin-bottom:10px;">
                    <h4>{title}</h4>
                    <p><b>Skill:</b> {skill}</p>
                    <p><b>Level:</b> {level}</p>
                    <p>{desc}</p>
                    </div>
                    """

                with tab1:
                    for skill in missing_skills:
                        st.markdown(card(
                            f"{skill.title()} Project",
                            skill,
                            "Beginner",
                            f"Build a simple project using {skill}"
                        ), unsafe_allow_html=True)

                with tab2:
                    for skill in missing_skills:
                        st.markdown(card(
                            f"{skill.title()} Project",
                            skill,
                            "Intermediate",
                            f"Apply {skill} on real dataset"
                        ), unsafe_allow_html=True)

                with tab3:
                    for skill in missing_skills:
                        st.markdown(card(
                            f"{skill.title()} Project",
                            skill,
                            "Advanced",
                            f"Build production-level system using {skill}"
                        ), unsafe_allow_html=True)

            shown += 1