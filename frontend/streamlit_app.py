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

# Custom CSS for beautiful modern UI
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main {
        background: transparent;
    }

    /* Content area - Clean white card */
    .block-container {
        padding: 3rem 2rem !important;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        margin: 2rem auto !important;
        max-width: 1400px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
    }

    /* Headers with modern gradient */
    h1 {
        color: transparent !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.25rem;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
    }

    /* Metric cards - Modern glassmorphism */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 20px 40px -12px rgba(102, 126, 234, 0.4);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px -12px rgba(102, 126, 234, 0.6);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        margin: 0.5rem 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .metric-label {
        font-size: 0.95rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    /* Buttons - Modern with hover effects */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.875rem 2.5rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.3px !important;
    }

    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px -5px rgba(102, 126, 234, 0.7) !important;
    }

    .stButton>button:active {
        transform: translateY(-1px) !important;
    }

    /* File uploader - Modern style */
    .stFileUploader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 16px !important;
        padding: 2.5rem !important;
        border: 2px dashed #cbd5e1 !important;
        transition: all 0.3s !important;
    }

    .stFileUploader:hover {
        border-color: #667eea !important;
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
    }

    /* Text area - Clean design */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s !important;
    }

    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Tabs - Modern style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        background: #f8fafc;
        border: 2px solid transparent;
        transition: all 0.3s;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        border-color: #e2e8f0;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Alert boxes - Modern design */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        padding: 1.25rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }

    /* Candidate card - Beautiful elevation */
    .candidate-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #f1f5f9;
    }

    .candidate-card:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        border-left-width: 8px;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }

    /* Sidebar - Dark elegant */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }

    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }

    /* Match score badges - Eye-catching */
    .match-score {
        display: inline-block;
        padding: 0.625rem 1.25rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.125rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        letter-spacing: 0.5px;
    }

    .score-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .score-good {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }

    .score-moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }

    .score-weak {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }

    /* Skill tags - Modern pills */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        color: #4338ca;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(67, 56, 202, 0.15);
        transition: all 0.3s;
    }

    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(67, 56, 202, 0.25);
    }

    /* Expander - Clean design */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        border: 1px solid #e2e8f0 !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        border-color: #cbd5e1 !important;
    }

    /* Metrics - Streamlit native */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Footer - Elegant */
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 2.5rem;
        font-size: 0.95rem;
        margin-top: 4rem;
        border-top: 2px solid #f1f5f9;
        font-weight: 500;
    }

    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem !important;
        transition: all 0.3s !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()


def main():
    """Main application entry point."""

    # Header with modern design
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 3rem 0;'>
        <h1 style='margin-bottom: 1rem;'>🎯 AI-Powered Resume Screening</h1>
        <p class='subtitle' style='max-width: 800px; margin: 0 auto;'>
            Intelligent Candidate Matching & Interview Scheduling<br>
            <span style='font-size: 1rem; color: #94a3b8;'>Powered by Azure OpenAI | ITC Infotech</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'parsed_resumes' not in st.session_state:
        st.session_state.parsed_resumes = []
    if 'match_results' not in st.session_state:
        st.session_state.match_results = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""

    # Sidebar with modern design
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);'>
            <h2 style='color: white; font-size: 1.5rem; margin: 0; font-weight: 800; letter-spacing: 1px;'>
                ITC INFOTECH
            </h2>
            <p style='color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0.5rem 0 0 0; font-weight: 500;'>
                AI Resume Screener
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: white; font-size: 1.1rem; margin-bottom: 1rem;'>🧭 Navigation</h3>", unsafe_allow_html=True)
        page = st.radio(
            "navigation",
            [
                "📊 Dashboard",
                "📤 Upload Resumes",
                "🎯 Match Candidates",
                "🏆 Top Candidates",
                "📅 Schedule Interviews",
                "📈 Analytics"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.1); margin: 1.5rem 0;'><br>", unsafe_allow_html=True)

        st.markdown("<h3 style='color: white; font-size: 1.1rem; margin-bottom: 1rem;'>⚙️ Settings</h3>", unsafe_allow_html=True)
        min_score = st.slider("Minimum Match Score", 0.0, 1.0, 0.5, 0.05)
        top_n = st.number_input("Top N Candidates", 1, 20, 10)

        st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.1); margin: 1.5rem 0;'><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; border-left: 3px solid #10b981;'>
            <p style='color: #10b981; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>💡 PRO TIP</p>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0; line-height: 1.4;'>
                Upload clear, well-formatted resumes for best AI matching results
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.1); margin: 1.5rem 0;'><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: center; opacity: 0.7;'>
            <p style='font-size: 0.8rem; margin: 0;'>🔐 Secured by</p>
            <p style='font-size: 0.9rem; margin: 0.3rem 0 0 0; font-weight: 600;'>Azure OpenAI</p>
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2rem;'>Upload candidate resumes for AI-powered analysis and matching</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Upload Files", "🌐 Fetch from Portal"])

    with tab1:
        st.markdown("### Upload Resume Files")

        st.markdown("""
        <div style='background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
                    padding: 1rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #3b82f6;'>
            <p style='margin: 0; color: #1e40af; font-weight: 500;'>
                <strong>📋 Supported Formats:</strong> PDF, DOCX, DOC<br>
                <strong>📊 Batch Upload:</strong> Multiple files at once<br>
                <strong>⚡ Processing:</strong> Powered by Azure OpenAI
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drop resume files here or click to browse",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            key="resume_uploader"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

            # Show file list
            st.markdown("**📄 Uploaded Files:**")
            for i, file in enumerate(uploaded_files, 1):
                st.markdown(f"{i}. `{file.name}` ({file.size / 1024:.1f} KB)")

            if st.button("🔍 Parse Resumes", type="primary", use_container_width=True):
                with st.spinner("🔄 Parsing resumes... This may take a moment..."):
                    parse_resumes(uploaded_files)

    with tab2:
        st.markdown("### Fetch from Job Portal")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f59e0b;'>
            <p style='margin: 0; color: #92400e; font-weight: 500; font-size: 1.05rem;'>
                🚧 <strong>Coming Soon!</strong><br><br>
                Portal integration with Naukri, LinkedIn, and other job portals is under development.
                Currently, you can upload resumes manually.
            </p>
        </div>
        """, unsafe_allow_html=True)


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
    st.markdown("<p style='color: #64748b; font-size: 1.05rem; margin-bottom: 2rem;'>Use AI-powered semantic matching to find the best candidates</p>", unsafe_allow_html=True)

    if not st.session_state.parsed_resumes:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                    padding: 2rem; border-radius: 12px; border-left: 4px solid #ef4444; text-align: center;'>
            <h3 style='color: #991b1b; margin: 0 0 0.5rem 0;'>⚠️ No Resumes Found</h3>
            <p style='margin: 0; color: #7f1d1d; font-size: 1.05rem;'>
                Please upload resumes first before matching candidates.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Status card
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
                padding: 1.25rem; border-radius: 12px; border-left: 4px solid #10b981; margin-bottom: 2rem;'>
        <p style='margin: 0; color: #065f46; font-weight: 600; font-size: 1.1rem;'>
            ✅ <strong>{len(st.session_state.parsed_resumes)} resumes</strong> ready for AI matching
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Job description input
    st.markdown("### 📝 Job Description")
    st.markdown("<p style='color: #64748b; margin-bottom: 1rem;'>Paste the complete job description including requirements, qualifications, and responsibilities</p>", unsafe_allow_html=True)

    job_description = st.text_area(
        "Enter or paste the complete job description",
        value=st.session_state.job_description,
        height=280,
        placeholder="Example:\n\nJob Title: Senior Python Developer\n\nRequirements:\n- 5+ years Python experience\n- FastAPI, Django, Flask\n- AWS, Docker, Kubernetes\n- Strong problem-solving skills\n...",
        label_visibility="collapsed"
    )

    st.session_state.job_description = job_description

    # Required skills (optional)
    st.markdown("### 🎯 Required Skills (Optional)")
    st.markdown("<p style='color: #64748b; margin-bottom: 1rem;'>Specify key skills for more accurate matching</p>", unsafe_allow_html=True)

    skills_input = st.text_input(
        "Enter required skills separated by commas",
        placeholder="Python, Machine Learning, AWS, Docker, Kubernetes, FastAPI...",
        label_visibility="collapsed"
    )

    required_skills = [s.strip() for s in skills_input.split(',') if s.strip()] if skills_input else None

    if required_skills:
        st.markdown("**Selected Skills:**")
        skills_html = " ".join([f"<span class='skill-tag'>{skill}</span>" for skill in required_skills])
        st.markdown(skills_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Match button
    if st.button("🚀 Start AI Matching", type="primary", use_container_width=True, disabled=not job_description):
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
