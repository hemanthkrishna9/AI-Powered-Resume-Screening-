"""
Streamlit Dashboard - Main Application with Rich UI/UX.

This is the main Streamlit application for the recruiter dashboard
with modern design and beautiful styling.
"""

import streamlit as st
import sys
from pathlib import Path
import os
import logging

# Add src to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import components
from src.resume_parser.parser import ResumeParser
from src.resume_parser.extractor import DataExtractor
from src.ai_matcher.matcher import ResumeMatcher
from src.ai_matcher.ranker import CandidateRanker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="AI Resume Screener - ITC Infotech",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
def load_css():
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }

    /* Content area */
    .block-container {
        padding: 2rem 3rem;
        background: white;
        border-radius: 20px;
        margin: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }

    /* Headers */
    h1 {
        color: #1e3a8a;
        font-weight: 800;
        font-size: 3rem !important;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #3b82f6;
        font-weight: 700;
        font-size: 2rem !important;
        margin-top: 2rem;
    }

    h3 {
        color: #6366f1;
        font-weight: 600;
        font-size: 1.5rem !important;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        text-align: center;
        transition: transform 0.3s;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
        font-size: 1.1rem;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* File uploader */
    .stFileUploader {
        background: #f8fafc;
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed #cbd5e1;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        font-size: 1rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }

    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
    }

    /* Candidate card */
    .candidate-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }

    .candidate-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }

    /* Match score badge */
    .match-score {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
    }

    .score-excellent {
        background: #10b981;
        color: white;
    }

    .score-good {
        background: #3b82f6;
        color: white;
    }

    .score-moderate {
        background: #f59e0b;
        color: white;
    }

    .score-weak {
        background: #ef4444;
        color: white;
    }

    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #4f46e5;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 2rem;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()


def main():
    """Main application entry point."""

    # Header
    st.markdown("<h1>🎯 AI-Powered Resume Screening</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Intelligent Candidate Matching & Interview Scheduling | Powered by Azure OpenAI</p>", unsafe_allow_html=True)

    # Initialize session state
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'parsed_resumes' not in st.session_state:
        st.session_state.parsed_resumes = []
    if 'match_results' not in st.session_state:
        st.session_state.match_results = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=ITC+Infotech", use_column_width=True)
        st.markdown("---")

        page = st.radio(
            "🧭 Navigation",
            [
                "📊 Dashboard",
                "📤 Upload Resumes",
                "🎯 Match Candidates",
                "🏆 Top Candidates",
                "📅 Schedule Interviews",
                "📈 Analytics"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        min_score = st.slider("Minimum Match Score", 0.0, 1.0, 0.5, 0.05)
        top_n = st.number_input("Top N Candidates", 1, 20, 10)

        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("📌 Upload clear, well-formatted resumes for best results")

        st.markdown("---")
        st.markdown("🔐 Powered by Azure OpenAI")

    # Main content
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📤 Upload Resumes":
        show_upload_page()
    elif page == "🎯 Match Candidates":
        show_matching_page(min_score, top_n)
    elif page == "🏆 Top Candidates":
        show_top_candidates(min_score, top_n)
    elif page == "📅 Schedule Interviews":
        show_scheduling_page()
    elif page == "📈 Analytics":
        show_analytics_page()

    # Footer
    st.markdown("---")
    st.markdown(
        "<div class='footer'>©2025 ITC Infotech. All Rights Reserved. | Powered by Azure OpenAI</div>",
        unsafe_allow_html=True
    )


def show_dashboard():
    """Show main dashboard."""
    st.markdown("## 📊 Dashboard Overview")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Resumes</div>
            <div class='metric-value'>{len(st.session_state.parsed_resumes)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        shortlisted = len([r for r in st.session_state.match_results if r.get('match_score', 0) >= 0.6])
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Shortlisted</div>
            <div class='metric-value'>{shortlisted}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Interviews</div>
            <div class='metric-value'>0</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Completed</div>
            <div class='metric-value'>0</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick actions
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Upload New Resumes", use_container_width=True):
            st.session_state.current_page = "upload"
            st.rerun()

    with col2:
        if st.button("🎯 Start Matching", use_container_width=True):
            st.session_state.current_page = "match"
            st.rerun()

    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()

    # Recent activity
    st.markdown("### 📋 Recent Activity")

    if st.session_state.match_results:
        for i, result in enumerate(st.session_state.match_results[:5]):
            score = result.get('match_score', 0)
            score_class = get_score_class(score)

            st.markdown(f"""
            <div class='candidate-card'>
                <strong>{result.get('candidate_name', 'Unknown Candidate')}</strong><br>
                <span class='match-score {score_class}'>{int(score * 100)}% Match</span><br>
                <small>{result.get('explanation', '')[:100]}...</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📌 No matching results yet. Upload resumes and create a match to get started!")


def show_upload_page():
    """Show resume upload page."""
    st.markdown("## 📤 Upload Resumes")

    tab1, tab2 = st.tabs(["📁 Upload Files", "🌐 Fetch from Portal"])

    with tab1:
        st.markdown("### Upload Resume Files")
        st.markdown("Supported formats: PDF, DOCX, DOC")

        uploaded_files = st.file_uploader(
            "Drop resume files here or click to browse",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            key="resume_uploader"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

            if st.button("🔍 Parse Resumes", type="primary", use_container_width=True):
                with st.spinner("🔄 Parsing resumes... This may take a moment..."):
                    parse_resumes(uploaded_files)

    with tab2:
        st.markdown("### Fetch from Job Portal")
        st.info("🚧 Portal integration coming soon! Currently supports manual upload.")


def parse_resumes(uploaded_files):
    """Parse uploaded resume files."""
    parser = ResumeParser()
    extractor = DataExtractor()

    progress_bar = st.progress(0)
    status_text = st.empty()

    parsed_count = 0

    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")

        try:
            # Save temporarily
            temp_path = ROOT_DIR / "data" / "resumes" / uploaded_file.name
            temp_path.parent.mkdir(parents=True, exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Parse
            parsed = parser.parse(temp_path)

            if parsed['status'] == 'success':
                # Extract data
                extracted = extractor.extract_all(parsed['raw_text'])
                extracted['file_name'] = uploaded_file.name
                extracted['id'] = f"resume_{idx}"

                st.session_state.parsed_resumes.append(extracted)
                parsed_count += 1

            progress_bar.progress((idx + 1) / len(uploaded_files))

        except Exception as e:
            logger.error(f"Error parsing {uploaded_file.name}: {e}")
            st.error(f"❌ Error parsing {uploaded_file.name}: {str(e)}")

    status_text.text("")
    progress_bar.empty()

    if parsed_count > 0:
        st.success(f"✅ Successfully parsed {parsed_count} resume(s)!")
        st.balloons()
    else:
        st.error("❌ No resumes were parsed successfully")


def show_matching_page(min_score, top_n):
    """Show candidate matching page."""
    st.markdown("## 🎯 Match Candidates to Job Description")

    if not st.session_state.parsed_resumes:
        st.warning("⚠️ No resumes uploaded yet! Please upload resumes first.")
        return

    st.markdown(f"**{len(st.session_state.parsed_resumes)} resumes** ready for matching")

    # Job description input
    st.markdown("### 📝 Job Description")
    job_description = st.text_area(
        "Enter or paste the complete job description",
        value=st.session_state.job_description,
        height=250,
        placeholder="Enter job title, required skills, experience, qualifications..."
    )

    st.session_state.job_description = job_description

    # Required skills (optional)
    st.markdown("### 🎯 Required Skills (Optional)")
    skills_input = st.text_input(
        "Enter required skills separated by commas",
        placeholder="Python, Machine Learning, AWS, Docker..."
    )

    required_skills = [s.strip() for s in skills_input.split(',') if s.strip()] if skills_input else None

    # Match button
    if st.button("🚀 Start Matching", type="primary", use_container_width=True, disabled=not job_description):
        with st.spinner("🧠 AI is analyzing candidates... This may take a minute..."):
            try:
                matcher = ResumeMatcher()
                results = matcher.batch_match(
                    st.session_state.parsed_resumes,
                    job_description,
                    required_skills
                )

                st.session_state.match_results = results
                st.success(f"✅ Matching complete! Found {len(results)} candidates")
                st.balloons()

            except Exception as e:
                logger.error(f"Matching error: {e}")
                st.error(f"❌ Error during matching: {str(e)}")


def show_top_candidates(min_score, top_n):
    """Show top candidates."""
    st.markdown("## 🏆 Top Matched Candidates")

    if not st.session_state.match_results:
        st.info("📌 No matching results yet. Go to 'Match Candidates' to start!")
        return

    # Filter and rank
    ranker = CandidateRanker(min_score=min_score)
    filtered = ranker.filter_by_score(st.session_state.match_results)
    top_candidates = ranker.get_top_n(filtered, top_n)

    st.markdown(f"### Showing top {len(top_candidates)} candidates (min score: {int(min_score * 100)}%)")

    for idx, candidate in enumerate(top_candidates):
        score = candidate.get('match_score', 0)
        score_class = get_score_class(score)

        with st.expander(f"#{idx + 1} - {candidate.get('candidate_name', 'Unknown')} - {int(score * 100)}% Match"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Match Score:** <span class='match-score {score_class}'>{int(score * 100)}%</span>", unsafe_allow_html=True)
                st.markdown(f"**Explanation:** {candidate.get('explanation', '')}")

                st.markdown("**Matching Skills:**")
                skills_html = " ".join([f"<span class='skill-tag'>{skill}</span>" for skill in candidate.get('matching_skills', [])])
                st.markdown(skills_html, unsafe_allow_html=True)

                if candidate.get('missing_skills'):
                    st.markdown(f"**Missing Skills:** {', '.join(candidate.get('missing_skills', [])[:5])}")

            with col2:
                st.metric("Experience", f"{candidate.get('total_experience', 0)} years")
                st.metric("Semantic Score", f"{int(candidate.get('semantic_score', 0) * 100)}%")
                st.metric("Skill Match", f"{int(candidate.get('skill_match_score', 0) * 100)}%")

                if st.button("📅 Schedule Interview", key=f"schedule_{idx}"):
                    st.success("Interview scheduling coming soon!")


def show_scheduling_page():
    """Show interview scheduling page."""
    st.markdown("## 📅 Schedule Interviews")
    st.info("🚧 Interview scheduling feature coming soon!")


def show_analytics_page():
    """Show analytics page."""
    st.markdown("## 📈 Analytics Dashboard")
    st.info("🚧 Analytics dashboard coming soon!")


def get_score_class(score):
    """Get CSS class for match score."""
    if score >= 0.8:
        return "score-excellent"
    elif score >= 0.6:
        return "score-good"
    elif score >= 0.4:
        return "score-moderate"
    else:
        return "score-weak"


if __name__ == "__main__":
    main()
