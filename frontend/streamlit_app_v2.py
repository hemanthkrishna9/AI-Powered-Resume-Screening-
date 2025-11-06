"""
ITC Infotech AI Resume Screener - Enterprise Edition
Professional, modern UI/UX following enterprise design standards
"""

import streamlit as st
import sys
from pathlib import Path
import os
import logging
from datetime import datetime

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

# Page config
st.set_page_config(
    page_title="ITC Infotech - AI Resume Screener",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_custom_css():
    """Load enterprise design system CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --primary-blue: #0066CC;
        --primary-dark: #003D7A;
        --accent-purple: #7C3AED;
        --bg-main: #F8FAFC;
        --bg-card: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #64748B;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --border-light: #E2E8F0;
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: var(--bg-main) !important;
    }

    .main .block-container {
        padding: 2rem 1.5rem !important;
        max-width: 1400px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header, .stDeployButton {display: none !important;}

    /* Top Header Bar */
    .top-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 102, 204, 0.1);
    }

    .top-header h1 {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .top-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 0 0 !important;
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
        height: 100%;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
    }

    .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .metric-trend {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }

    .trend-up { color: var(--success); }
    .trend-down { color: var(--error); }

    /* Action Cards */
    .action-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid var(--border-light);
        height: 100%;
    }

    .action-card:hover {
        border-color: var(--primary-blue);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 102, 204, 0.15);
    }

    .action-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .action-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .action-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }

    /* Activity Feed */
    .activity-feed {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-light);
    }

    .activity-item {
        display: flex;
        align-items: start;
        padding: 1rem;
        border-left: 3px solid var(--border-light);
        margin-left: 1rem;
        position: relative;
    }

    .activity-item::before {
        content: "";
        position: absolute;
        left: -7px;
        top: 1rem;
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background: var(--primary-blue);
        border: 3px solid white;
    }

    .activity-content {
        margin-left: 1rem;
        flex: 1;
    }

    .activity-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .activity-time {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 102, 204, 0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 102, 204, 0.3) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid var(--border-light) !important;
        padding: 1.5rem 1rem !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        margin: 0.25rem 0 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: var(--bg-main) !important;
    }

    section[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }

    /* Charts */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .chart-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-success {
        background: #ECFDF5;
        color: #047857;
    }

    .badge-warning {
        background: #FFFBEB;
        color: #92400E;
    }

    .badge-info {
        background: #EFF6FF;
        color: #1E40AF;
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed var(--border-light) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        background: white !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader:hover {
        border-color: var(--primary-blue) !important;
        background: #F0F9FF !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid var(--border-light) !important;
        padding: 0.75rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()


def main():
    """Main application entry point"""

    # Initialize session state
    if 'resumes' not in st.session_state:
        st.session_state.resumes = []
    if 'parsed_resumes' not in st.session_state:
        st.session_state.parsed_resumes = []
    if 'match_results' not in st.session_state:
        st.session_state.match_results = []
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""

    # Sidebar Navigation
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0 2rem 0; border-bottom: 1px solid var(--border-light); margin-bottom: 1.5rem;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
            <h2 style='color: var(--primary-blue); font-size: 1.25rem; font-weight: 800; margin: 0;'>ITC INFOTECH</h2>
            <p style='color: var(--text-secondary); font-size: 0.875rem; margin: 0.25rem 0 0 0;'>AI Resume Screener</p>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        page = st.radio(
            "Navigation",
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

        # Settings section
        st.markdown("<br><hr style='margin: 1.5rem 0; border-color: var(--border-light);'><br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        min_score = st.slider("Minimum Match Score", 0.0, 1.0, 0.5, 0.05)
        top_n = st.number_input("Top N Candidates", 1, 20, 10)

        # Pro tip
        st.markdown("<br><hr style='margin: 1.5rem 0; border-color: var(--border-light);'><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: #EFF6FF; padding: 1rem; border-radius: 8px; border-left: 4px solid var(--primary-blue);'>
            <p style='color: var(--primary-blue); font-weight: 600; margin: 0 0 0.5rem 0; font-size: 0.875rem;'>💡 PRO TIP</p>
            <p style='color: var(--text-secondary); font-size: 0.8rem; margin: 0; line-height: 1.5;'>
                Upload resumes in batch for faster processing. PDF and DOCX formats work best!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Main Content
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


def show_dashboard():
    """Enterprise Dashboard with Modern Design"""

    # Header
    st.markdown(f"""
    <div class='top-header'>
        <h1>👋 Welcome back, Recruiter!</h1>
        <p>Here's what's happening with your recruitment today - {datetime.now().strftime("%B %d, %Y")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-icon' style='background: #EFF6FF; color: #0066CC;'>📄</div>
            <div class='metric-label'>Total Resumes</div>
            <div class='metric-value'>{}</div>
            <div class='metric-trend trend-up'>↗ +23 from last week</div>
        </div>
        """.format(len(st.session_state.parsed_resumes)), unsafe_allow_html=True)

    with col2:
        shortlisted = len([r for r in st.session_state.match_results if r.get('match_score', 0) >= 0.6])
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-icon' style='background: #ECFDF5; color: #10B981;'>✓</div>
            <div class='metric-label'>Shortlisted</div>
            <div class='metric-value'>{}</div>
            <div class='metric-trend trend-up'>↗ {}% of total</div>
        </div>
        """.format(shortlisted, int((shortlisted / max(len(st.session_state.parsed_resumes), 1)) * 100)), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-icon' style='background: #F5F3FF; color: #7C3AED;'>📅</div>
            <div class='metric-label'>Interviews Scheduled</div>
            <div class='metric-value'>0</div>
            <div class='metric-trend trend-up'>↗ 0 upcoming</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-icon' style='background: #ECFEFF; color: #0891B2;'>✅</div>
            <div class='metric-label'>Completed</div>
            <div class='metric-value'>0</div>
            <div class='metric-trend trend-up'>↗ 0% success rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='action-card' onclick='window.location.reload()'>
            <div class='action-icon'>📤</div>
            <div class='action-title'>Upload Resumes</div>
            <div class='action-description'>Add new candidates to the system</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>🎯</div>
            <div class='action-title'>Start Matching</div>
            <div class='action-description'>Find best candidates for roles</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>📊</div>
            <div class='action-title'>View Analytics</div>
            <div class='action-description'>Detailed recruitment insights</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent Activity
    st.markdown("### 📋 Recent Activity")
    st.markdown("""
    <div class='activity-feed'>
        <div class='activity-item'>
            <div class='activity-content'>
                <div class='activity-title'>15 new resumes uploaded</div>
                <div class='activity-time'>2 hours ago</div>
            </div>
        </div>
        <div class='activity-item'>
            <div class='activity-content'>
                <div class='activity-title'>Interview scheduled with John Doe</div>
                <div class='activity-time'>3 hours ago</div>
            </div>
        </div>
        <div class='activity-item'>
            <div class='activity-content'>
                <div class='activity-title'>Sarah Smith marked as shortlisted</div>
                <div class='activity-time'>5 hours ago</div>
            </div>
        </div>
        <div class='activity-item'>
            <div class='activity-content'>
                <div class='activity-title'>23 candidates matched for "Senior Developer"</div>
                <div class='activity-time'>1 day ago</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_upload_page():
    """Upload page with modern design"""
    st.markdown("<h1>📤 Upload Resumes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); font-size: 1.125rem;'>Upload candidate resumes for AI-powered analysis</p><br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Upload Files", "🌐 Bulk Import"])

    with tab1:
        uploaded_files = st.file_uploader(
            "Drop resume files here or click to browse",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            key="resume_uploader"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

            for i, file in enumerate(uploaded_files, 1):
                st.markdown(f"{i}. `{file.name}` ({file.size / 1024:.1f} KB)")

            if st.button("🔍 Parse All Resumes", type="primary"):
                with st.spinner("🔄 Processing resumes..."):
                    parse_resumes(uploaded_files)

    with tab2:
        st.info("🚧 Bulk import from job portals coming soon!")


def parse_resumes(uploaded_files):
    """Parse uploaded resumes"""
    parser = ResumeParser()
    extractor = DataExtractor()

    progress_bar = st.progress(0)
    status_text = st.empty()

    parsed_count = 0

    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")

        try:
            temp_path = ROOT_DIR / "data" / "resumes" / uploaded_file.name
            temp_path.parent.mkdir(parents=True, exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            parsed = parser.parse(temp_path)

            if parsed['status'] == 'success':
                extracted = extractor.extract_all(parsed['raw_text'])
                extracted['file_name'] = uploaded_file.name
                extracted['id'] = f"resume_{idx}"

                st.session_state.parsed_resumes.append(extracted)
                parsed_count += 1

            progress_bar.progress((idx + 1) / len(uploaded_files))

        except Exception as e:
            logger.error(f"Error parsing {uploaded_file.name}: {e}")
            st.error(f"❌ Error: {uploaded_file.name}")

    status_text.text("")
    progress_bar.empty()

    if parsed_count > 0:
        st.success(f"✅ Successfully parsed {parsed_count} resumes!")
        st.balloons()


def show_matching_page(min_score, top_n):
    """Matching page placeholder"""
    st.markdown("<h1>🎯 Match Candidates</h1>", unsafe_allow_html=True)
    st.info("Matching functionality coming in next phase")


def show_top_candidates(min_score, top_n):
    """Top candidates placeholder"""
    st.markdown("<h1>🏆 Top Candidates</h1>", unsafe_allow_html=True)
    st.info("Top candidates view coming in next phase")


def show_scheduling_page():
    """Scheduling placeholder"""
    st.markdown("<h1>📅 Schedule Interviews</h1>", unsafe_allow_html=True)
    st.info("Interview scheduling coming in next phase")


def show_analytics_page():
    """Analytics placeholder"""
    st.markdown("<h1>📈 Analytics</h1>", unsafe_allow_html=True)
    st.info("Analytics dashboard coming in next phase")


if __name__ == "__main__":
    main()
