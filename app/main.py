"""Main Streamlit application for Innovation Scorer."""

from __future__ import annotations

import sys
from pathlib import Path

# Add the app directory to Python path for imports
app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

import streamlit as st
import pandas as pd

from config import ScoringConfig
from scoring import ScoringEngine
from utils import load_data_file
from ui_components import (
    render_event_settings,
    render_scoring_weights,
    render_thresholds,
    render_company_list,
    render_disqualification_patterns,
    render_themes,
    render_topic_keyword_packs,
    render_subthemes,
    build_config_from_ui,
)

# Page configuration
st.set_page_config(
    page_title="Innovation Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "config" not in st.session_state:
        st.session_state.config = ScoringConfig.get_default()
    if "scored_data" not in st.session_state:
        st.session_state.scored_data = None
    if "top_data" not in st.session_state:
        st.session_state.top_data = None
    if "stats" not in st.session_state:
        st.session_state.stats = None


def render_sidebar():
    """Render the configuration sidebar."""
    with st.sidebar:
        st.title("Configuration")
        
        # Config file operations
        st.markdown("---")
        st.subheader("Config Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download current config
            config_json = st.session_state.config.to_json()
            st.download_button(
                label="Download Config",
                data=config_json,
                file_name="scoring_config.json",
                mime="application/json",
                help="Download current configuration as JSON"
            )
        
        with col2:
            # Reset to defaults
            if st.button("Reset Defaults", help="Reset all settings to defaults"):
                st.session_state.config = ScoringConfig.get_default()
                st.rerun()
        
        # Upload config
        uploaded_config = st.file_uploader(
            "Upload Config Template",
            type=["json"],
            help="Upload a previously saved configuration"
        )
        
        if uploaded_config is not None:
            try:
                config_str = uploaded_config.read().decode("utf-8")
                st.session_state.config = ScoringConfig.from_json(config_str)
                st.success("Configuration loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading config: {e}")
        
        st.markdown("---")
        
        # Configuration sections in expanders
        config = st.session_state.config
        
        with st.expander("Event Settings", expanded=True):
            event_settings = render_event_settings(config)
        
        with st.expander("Scoring Weights"):
            scoring_weights = render_scoring_weights(config)
        
        with st.expander("Thresholds"):
            thresholds = render_thresholds(config)
        
        with st.expander("Company Allowlist"):
            company_settings = render_company_list(config)
        
        with st.expander("Disqualification Patterns"):
            disqualification = render_disqualification_patterns(config)
        
        with st.expander("Themes & Keywords"):
            themes = render_themes(config)
        
        with st.expander("Topic Keyword Packs"):
            topic_packs = render_topic_keyword_packs(config)
        
        with st.expander("Subthemes"):
            subthemes = render_subthemes(config)
        
        # Build and store updated config
        st.session_state.config = build_config_from_ui(
            event_settings,
            scoring_weights,
            thresholds,
            company_settings,
            disqualification,
            themes,
            topic_packs,
            subthemes,
        )


def render_main_content():
    """Render the main content area."""
    # Header
    st.markdown('<p class="main-header">Innovation Scorer</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Score and rank LinkedIn profiles for innovation events</p>',
        unsafe_allow_html=True
    )
    
    # File upload section
    st.markdown("### Upload Profiles")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file with LinkedIn profiles",
        type=["csv", "xlsx", "xls"],
        help="File should contain columns: fullName, title, companyName, summary, titleDescription"
    )
    
    if uploaded_file is not None:
        # Show file info
        st.info(f"Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
        
        # Run scoring button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            run_scoring = st.button("Run Scoring", type="primary", use_container_width=True)
        with col2:
            preview_data = st.button("Preview Data", use_container_width=True)
        
        if preview_data:
            try:
                df, _ = load_data_file(uploaded_file)
                st.markdown("### Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Showing first 10 of {len(df)} rows")
            except Exception as e:
                st.error(f"Error loading file: {e}")
        
        if run_scoring:
            with st.spinner("Scoring profiles..."):
                try:
                    # Load data
                    df, event_topic_from_cell = load_data_file(uploaded_file)
                    
                    # Create scoring engine with current config
                    engine = ScoringEngine(st.session_state.config)
                    
                    # Run scoring
                    scored_sorted, top, stats = engine.score_dataframe(df)
                    
                    # Store results
                    st.session_state.scored_data = scored_sorted
                    st.session_state.top_data = top
                    st.session_state.stats = stats
                    
                    st.success("Scoring complete!")
                    
                except Exception as e:
                    st.error(f"Error during scoring: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Results section
    if st.session_state.stats is not None:
        st.markdown("---")
        st.markdown("### Results")
        
        stats = st.session_state.stats
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Profiles", stats["total_profiles"])
        with col2:
            st.metric("Eligible Profiles", stats["eligible_profiles"])
        with col3:
            st.metric(f"Top {stats['top_n']}", stats["top_n"])
        with col4:
            st.metric("Company Failures", stats["top_n_company_failures"])
        
        # Event info
        with st.expander("Scoring Configuration Used"):
            st.markdown(f"**Event Topic:** {stats['event_topic']}")
            st.markdown(f"**Dynamic Keywords:** {', '.join(stats['dynamic_keywords']) if stats['dynamic_keywords'] else 'None'}")
            st.markdown(f"**Themes:** {', '.join(stats['themes'])}")
        
        # Results tabs
        tab1, tab2 = st.tabs([f"Top {stats['top_n']} Profiles", "All Eligible Profiles"])
        
        with tab1:
            if st.session_state.top_data is not None and len(st.session_state.top_data) > 0:
                # Select columns to display
                display_cols = ["fullName_export", "title", "companyName", "company_matched_canonical", "total_score"]
                available_cols = [c for c in display_cols if c in st.session_state.top_data.columns]
                
                st.dataframe(
                    st.session_state.top_data[available_cols],
                    use_container_width=True,
                    height=400
                )
            else:
                st.warning("No eligible profiles found.")
        
        with tab2:
            if st.session_state.scored_data is not None and len(st.session_state.scored_data) > 0:
                display_cols = ["fullName_export", "title", "companyName", "total_score", "is_vp", "is_head", "theme_points"]
                available_cols = [c for c in display_cols if c in st.session_state.scored_data.columns]
                
                st.dataframe(
                    st.session_state.scored_data[available_cols],
                    use_container_width=True,
                    height=400
                )
            else:
                st.warning("No eligible profiles found.")
        
        # Download section
        st.markdown("### Download Results")
        
        if st.session_state.scored_data is not None:
            engine = ScoringEngine(st.session_state.config)
            excel_data = engine.export_to_excel(
                st.session_state.scored_data,
                st.session_state.top_data
            )
            
            st.download_button(
                label="Download Excel Report",
                data=excel_data,
                file_name="innovation_roundtable_scored_profiles.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )


def main():
    """Main application entry point."""
    init_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
