"""
Streamlit Dashboard - Main Application.

This is the main Streamlit application for the recruiter dashboard.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="AI Resume Screener",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🤖 AI-Powered Resume Screening & Interview Scheduling")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Go to",
            [
                "Dashboard",
                "Upload Resumes",
                "Match Candidates",
                "Schedule Interviews",
                "Analytics"
            ]
        )

    # Main content
    if page == "Dashboard":
        show_dashboard()
    elif page == "Upload Resumes":
        show_upload_page()
    elif page == "Match Candidates":
        show_matching_page()
    elif page == "Schedule Interviews":
        show_scheduling_page()
    elif page == "Analytics":
        show_analytics_page()


def show_dashboard():
    """Show dashboard page."""
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Resumes", "0", "0")
    with col2:
        st.metric("Shortlisted", "0", "0")
    with col3:
        st.metric("Interviews Scheduled", "0", "0")
    with col4:
        st.metric("Completed", "0", "0")

    st.markdown("---")
    st.info("Welcome to the AI Resume Screening Dashboard!")
    st.write("Upload a job description and resumes to get started.")


def show_upload_page():
    """Show resume upload page."""
    st.header("📤 Upload Resumes")

    tab1, tab2 = st.tabs(["Upload Files", "Fetch from Portal"])

    with tab1:
        st.subheader("Upload Resume Files")

        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
            for file in uploaded_files:
                st.write(f"- {file.name}")

    with tab2:
        st.subheader("Fetch from Job Portal")
        st.info("Portal integration coming soon!")


def show_matching_page():
    """Show candidate matching page."""
    st.header("🎯 Match Candidates")

    st.subheader("Job Description")
    jd_text = st.text_area(
        "Enter or paste job description",
        height=200,
        placeholder="Paste the job description here..."
    )

    if st.button("Find Matching Candidates", type="primary"):
        if jd_text:
            with st.spinner("Analyzing candidates..."):
                st.info("Matching functionality will be implemented in the next phase")
        else:
            st.warning("Please enter a job description")


def show_scheduling_page():
    """Show interview scheduling page."""
    st.header("📅 Schedule Interviews")

    st.info("Select candidates to schedule interviews")

    # Placeholder for candidate list
    st.write("No candidates selected yet")


def show_analytics_page():
    """Show analytics page."""
    st.header("📈 Analytics")

    st.info("Analytics dashboard coming soon!")


if __name__ == "__main__":
    main()
