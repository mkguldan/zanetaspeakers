"""Reusable Streamlit UI components for configuration editing."""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict

from config import ScoringConfig


def render_event_settings(config: ScoringConfig) -> dict[str, Any]:
    """Render event settings section and return updated values."""
    st.subheader("Event Settings")
    
    event_name = st.text_input(
        "Event Name",
        value=config.event_name,
        help="Name of the innovation event"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.text_input(
            "Event Date",
            value=config.event_date,
            help="Date of the event"
        )
    with col2:
        event_location = st.text_input(
            "Location",
            value=config.event_location,
            help="Event location"
        )
    
    event_host = st.text_input(
        "Event Host",
        value=config.event_host,
        help="Company hosting the event"
    )
    
    event_topic_override = st.text_area(
        "Event Topic Override",
        value=config.event_topic_override,
        help="Override the event topic (used for dynamic keyword matching)"
    )
    
    main_theme = st.text_area(
        "Main Theme",
        value=config.main_theme,
        help="Main theme of the event"
    )
    
    return {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "event_host": event_host,
        "event_topic_override": event_topic_override,
        "main_theme": main_theme,
    }


def render_scoring_weights(config: ScoringConfig) -> dict[str, Any]:
    """Render scoring weights section and return updated values."""
    st.subheader("Scoring Weights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        w_senior_top = st.slider(
            "VP/Director Weight",
            min_value=0, max_value=100,
            value=config.w_senior_top,
            help="Weight for VP and innovation-focused Director titles"
        )
        
        w_head = st.slider(
            "Head of Dept Weight",
            min_value=0, max_value=100,
            value=config.w_head,
            help="Weight for Head of department titles"
        )
        
        w_title_innov = st.slider(
            "Title Innovation Weight",
            min_value=0, max_value=100,
            value=config.w_title_innov,
            help="Weight for innovation keywords in title"
        )
        
        w_text_innov = st.slider(
            "Text Innovation Weight",
            min_value=0, max_value=100,
            value=config.w_text_innov,
            help="Weight for innovation signals in text"
        )
    
    with col2:
        w_theme_hit = st.slider(
            "Theme Hit Points",
            min_value=0, max_value=20,
            value=config.w_theme_hit,
            help="Points per theme keyword hit"
        )
        
        w_theme_bonus = st.slider(
            "Theme Bonus (2+ hits)",
            min_value=0, max_value=20,
            value=config.w_theme_bonus,
            help="Bonus points for 2+ hits in a theme"
        )
        
        max_theme_points = st.slider(
            "Max Theme Points",
            min_value=10, max_value=100,
            value=config.max_theme_points,
            help="Maximum points from theme matches"
        )
        
        penalty_anti_function = st.slider(
            "Anti-Function Penalty",
            min_value=-100, max_value=0,
            value=config.penalty_anti_function,
            help="Penalty for anti-function keywords in title"
        )
    
    st.markdown("**Event Angle Weights**")
    col3, col4 = st.columns(2)
    with col3:
        w_title_event_hit = st.slider(
            "Title Event Hit Points",
            min_value=0, max_value=20,
            value=config.w_title_event_hit,
            help="Points for event-angle keywords in title"
        )
    with col4:
        max_title_event_points = st.slider(
            "Max Title Event Points",
            min_value=0, max_value=50,
            value=config.max_title_event_points,
            help="Maximum event-angle points in title"
        )
    
    return {
        "w_senior_top": w_senior_top,
        "w_head": w_head,
        "w_title_innov": w_title_innov,
        "w_text_innov": w_text_innov,
        "w_theme_hit": w_theme_hit,
        "w_theme_bonus": w_theme_bonus,
        "max_theme_points": max_theme_points,
        "penalty_anti_function": penalty_anti_function,
        "w_title_event_hit": w_title_event_hit,
        "max_title_event_points": max_title_event_points,
    }


def render_thresholds(config: ScoringConfig) -> dict[str, Any]:
    """Render threshold settings and return updated values."""
    st.subheader("Thresholds")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_theme_hits = st.number_input(
            "Min Theme Hits",
            min_value=0, max_value=10,
            value=config.min_theme_hits_total,
            help="Minimum total theme hits required"
        )
    
    with col2:
        min_innov_signals = st.number_input(
            "Min Innovation Signals",
            min_value=0, max_value=10,
            value=config.min_innov_signals_text,
            help="Minimum innovation signals in text"
        )
    
    with col3:
        top_n = st.number_input(
            "Top N Export",
            min_value=10, max_value=1000,
            value=config.top_n,
            help="Number of top profiles to export"
        )
    
    return {
        "min_theme_hits_total": min_theme_hits,
        "min_innov_signals_text": min_innov_signals,
        "top_n": top_n,
    }


def render_company_list(config: ScoringConfig) -> dict[str, Any]:
    """Render company allowlist editor and return updated values."""
    st.subheader("Company Allowlist")
    
    companies_text = st.text_area(
        "Allowed Companies (one per line)",
        value="\n".join(config.allowed_companies),
        height=200,
        help="List of allowed company names"
    )
    
    allowed_companies = [c.strip() for c in companies_text.split("\n") if c.strip()]
    
    st.markdown("**Company Variants (JSON)**")
    st.caption("Map variant names to canonical company names")
    import json
    variants_json = st.text_area(
        "Company Variants JSON",
        value=json.dumps(config.company_variants, indent=2),
        height=150,
        help="JSON mapping of canonical names to variant lists",
        label_visibility="collapsed"
    )
    try:
        company_variants = json.loads(variants_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format for company variants")
        company_variants = config.company_variants
    
    return {
        "allowed_companies": allowed_companies,
        "company_variants": company_variants,
    }


def render_disqualification_patterns(config: ScoringConfig) -> dict[str, Any]:
    """Render disqualification pattern editors and return updated values."""
    st.subheader("Title Disqualification Patterns")
    
    st.markdown("**Business Function Exclusions**")
    bus_text = st.text_area(
        "Business patterns (regex, one per line)",
        value="\n".join(config.disqualify_title_bus),
        height=150,
        help="Regex patterns to exclude business-focused titles"
    )
    disqualify_bus = [p.strip() for p in bus_text.split("\n") if p.strip()]
    
    st.markdown("**Technical Role Exclusions**")
    tech_text = st.text_area(
        "Technical patterns (regex, one per line)",
        value="\n".join(config.disqualify_title_tech),
        height=150,
        help="Regex patterns to exclude technical-focused titles"
    )
    disqualify_tech = [p.strip() for p in tech_text.split("\n") if p.strip()]
    
    return {
        "disqualify_title_bus": disqualify_bus,
        "disqualify_title_tech": disqualify_tech,
    }


def render_themes(config: ScoringConfig) -> dict[str, Any]:
    """Render themes editor and return updated values."""
    st.subheader("🎯 Core Themes (Always Active)")
    st.caption(
        "These themes are **always active** regardless of event topic. "
        "Keep this minimal - just core innovation focus. "
        "Event-specific themes come from **Topic Keyword Packs** below."
    )
    
    import json
    
    themes_json = st.text_area(
        "Core Themes (JSON)",
        value=json.dumps(config.themes, indent=2),
        height=200,
        help="JSON mapping of theme names to keyword lists. Keep minimal for flexibility.",
        label_visibility="collapsed"
    )
    
    try:
        themes = json.loads(themes_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format for themes")
        themes = config.themes
    
    return {"themes": themes}


def render_topic_keyword_packs(config: ScoringConfig) -> dict[str, Any]:
    """Render topic keyword packs editor and return updated values."""
    st.subheader("📦 Topic Keyword Packs (Dynamic Event Themes)")
    st.info(
        "🔑 **How it works:** When your **Event Topic** contains a key (e.g., 'sustainability'), "
        "the matching keywords are added to an **'Event Angle (Dynamic)'** theme.\n\n"
        "**Example:** Event Topic = 'Circularity, Net Zero & Subscription Models'\n"
        "→ Activates: 'circular', 'net zero', 'subscription' packs"
    )
    
    import json
    
    packs_json = st.text_area(
        "Keyword Packs (JSON)",
        value=json.dumps(config.topic_keyword_packs, indent=2),
        height=400,
        help="JSON mapping of trigger keys to keyword lists. Keys are matched against Event Topic.",
        label_visibility="collapsed"
    )
    
    try:
        packs = json.loads(packs_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format for keyword packs")
        packs = config.topic_keyword_packs
    
    return {"topic_keyword_packs": packs}


def render_subthemes(config: ScoringConfig) -> dict[str, Any]:
    """Render subthemes editor and return updated values."""
    st.subheader("Subthemes")
    
    subthemes_text = st.text_area(
        "Subthemes (one per line)",
        value="\n".join(config.subthemes),
        height=150,
        help="List of subthemes for the event"
    )
    
    subthemes = [s.strip() for s in subthemes_text.split("\n") if s.strip()]
    
    return {"subthemes": subthemes}


def build_config_from_ui(
    event_settings: dict,
    scoring_weights: dict,
    thresholds: dict,
    company_settings: dict,
    disqualification: dict,
    themes: dict,
    topic_packs: dict,
    subthemes: dict,
) -> ScoringConfig:
    """Build a ScoringConfig from all UI component outputs."""
    return ScoringConfig(
        # Event settings
        event_name=event_settings["event_name"],
        event_date=event_settings["event_date"],
        event_location=event_settings["event_location"],
        event_host=event_settings["event_host"],
        event_topic_override=event_settings["event_topic_override"],
        main_theme=event_settings["main_theme"],
        
        # Scoring weights
        w_senior_top=scoring_weights["w_senior_top"],
        w_head=scoring_weights["w_head"],
        w_title_innov=scoring_weights["w_title_innov"],
        w_text_innov=scoring_weights["w_text_innov"],
        w_theme_hit=scoring_weights["w_theme_hit"],
        w_theme_bonus=scoring_weights["w_theme_bonus"],
        max_theme_points=scoring_weights["max_theme_points"],
        penalty_anti_function=scoring_weights["penalty_anti_function"],
        w_title_event_hit=scoring_weights["w_title_event_hit"],
        max_title_event_points=scoring_weights["max_title_event_points"],
        
        # Thresholds
        min_theme_hits_total=thresholds["min_theme_hits_total"],
        min_innov_signals_text=thresholds["min_innov_signals_text"],
        top_n=thresholds["top_n"],
        
        # Company settings
        allowed_companies=company_settings["allowed_companies"],
        company_variants=company_settings["company_variants"],
        
        # Disqualification
        disqualify_title_bus=disqualification["disqualify_title_bus"],
        disqualify_title_tech=disqualification["disqualify_title_tech"],
        
        # Themes
        themes=themes["themes"],
        
        # Topic packs
        topic_keyword_packs=topic_packs["topic_keyword_packs"],
        
        # Subthemes
        subthemes=subthemes["subthemes"],
    )
