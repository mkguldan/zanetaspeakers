"""Scoring engine for Innovation Roundtable profile ranking."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

import pandas as pd

from config import (
    ScoringConfig,
    VP_PATTERNS,
    DIRECTOR_INNOV_PATTERNS,
    HEAD_PATTERNS,
    INNOV_RD_STRONG,
    TITLE_INNOV_RD,
    ANTI_FUNCTION,
)
from utils import (
    CompanyMatcher,
    safe_text,
    cregex,
    any_match,
    count_unique_hits,
    pick_col,
    process_names,
    sanitize_for_excel,
)


class ScoringEngine:
    """Engine for scoring LinkedIn profiles based on configurable criteria."""
    
    def __init__(self, config: ScoringConfig):
        """Initialize the scoring engine with a configuration."""
        self.config = config
        
        # Build company matcher
        self.company_matcher = CompanyMatcher(
            config.allowed_companies,
            config.company_variants
        )
        
        # Compile regex patterns
        self.vp_patterns = cregex(VP_PATTERNS)
        self.director_innov_patterns = cregex(DIRECTOR_INNOV_PATTERNS)
        self.head_patterns = cregex(HEAD_PATTERNS)
        self.innov_rd_strong = cregex(INNOV_RD_STRONG)
        self.title_innov_rd = cregex(TITLE_INNOV_RD)
        self.anti_function = cregex(ANTI_FUNCTION)
        
        # Compile disqualification patterns from config
        self.disqualify_title_bus = cregex(config.disqualify_title_bus)
        self.disqualify_title_tech = cregex(config.disqualify_title_tech)
        
        # Build theme patterns from config
        self.theme_patterns = {
            theme: [re.compile(re.escape(k), flags=re.IGNORECASE) for k in keywords]
            for theme, keywords in config.themes.items()
        }
        
        # Build dynamic event-angle theme
        self._build_dynamic_theme()
    
    def _build_dynamic_theme(self):
        """Build dynamic event-angle theme based on topic keyword packs."""
        event_topic = self._resolve_event_topic()
        topic_lower = event_topic.lower()
        
        dynamic_keywords = []
        for key_substr, keywords in self.config.topic_keyword_packs.items():
            if key_substr.lower() in topic_lower:
                dynamic_keywords.extend(keywords)
        
        # De-duplicate while preserving order
        seen = set()
        dynamic_keywords = [
            k for k in dynamic_keywords 
            if not (k.lower() in seen or seen.add(k.lower()))
        ]
        
        if dynamic_keywords:
            self.theme_patterns["Event Angle (Dynamic)"] = [
                re.compile(re.escape(k), flags=re.IGNORECASE) 
                for k in dynamic_keywords
            ]
        
        self.dynamic_keywords = dynamic_keywords
        self.event_topic = event_topic
    
    def _resolve_event_topic(self) -> str:
        """Resolve the event topic from configuration."""
        t = (self.config.event_topic_override or "").strip()
        if t:
            return t
        return (self.config.event_name or "").strip()
    
    def _get_search_cols(self, df: pd.DataFrame) -> list[str]:
        """Identify searchable columns in the DataFrame."""
        col_title = pick_col(df, ["title"])
        col_summary = pick_col(df, ["summary"])
        col_tdesc = pick_col(df, ["titledescription", "title description", "title_desc", "title desc", "role description"])
        
        search_cols = [c for c in [col_title, col_summary, col_tdesc] if c is not None]
        if not search_cols:
            raise ValueError("No searchable columns found (expected title/summary/titleDescription).")
        
        return search_cols
    
    def _row_blob(self, row: pd.Series, search_cols: list[str]) -> str:
        """Combine searchable columns into a single text blob."""
        parts = [safe_text(row.get(c, "")) for c in search_cols]
        return " \n ".join([p for p in parts if p]).strip()
    
    def _base_result(self) -> dict[str, Any]:
        """Create a base result dictionary with default values."""
        r = {
            "eligible": False,
            "total_score": -10_000,
            
            # Company debug
            "company_ok": False,
            "company_matched_canonical": "",
            "company_match_reason": "",
            
            # Title disqualification
            "title_disqualified": False,
            "title_disqualified_reason": "",
            
            # Seniority flags
            "is_vp": False,
            "is_dir_innov": False,
            "is_head": False,
            "is_senior": False,
            
            # Innovation
            "title_innov_rd": False,
            "innov_signals_text": 0,
            
            # Themes + scoring
            "theme_points": 0,
            "anti_function_title": False,
            "title_event_points": 0,
        }
        
        # Add theme hit columns
        for theme in self.theme_patterns.keys():
            r[f"{theme} hits"] = 0
        
        return r
    
    def _score_row(self, row: pd.Series, col_title: str, search_cols: list[str]) -> dict[str, Any]:
        """Score a single row."""
        result = self._base_result()
        
        # 1) COMPANY CHECK (HARD GATE)
        company_name = safe_text(row.get("companyName", ""))
        company_ok, canon, reason = self.company_matcher.match(company_name)
        
        result["company_ok"] = company_ok
        result["company_matched_canonical"] = canon
        result["company_match_reason"] = reason
        
        if not company_ok:
            return result
        
        # 2) TITLE DISQUALIFICATION (TITLE ONLY)
        title = safe_text(row.get(col_title, ""))
        
        disq_bus = any_match(self.disqualify_title_bus, title)
        disq_tech = any_match(self.disqualify_title_tech, title)
        if disq_bus or disq_tech:
            result["title_disqualified"] = True
            result["title_disqualified_reason"] = "business_function" if disq_bus else "too_technical"
            return result
        
        # 3) SENIORITY
        is_vp = any_match(self.vp_patterns, title)
        is_dir_innov = any_match(self.director_innov_patterns, title)
        is_head = any_match(self.head_patterns, title)
        
        is_senior = bool(is_vp or is_dir_innov or is_head)
        
        result["is_vp"] = is_vp
        result["is_dir_innov"] = is_dir_innov
        result["is_head"] = is_head
        result["is_senior"] = is_senior
        
        # NOTE: Seniority is NO LONGER a hard gate - it only adds bonus points
        # This allows relevant ICs/managers/specialists to remain eligible
        
        # 4) INNOVATION SIGNAL
        text = self._row_blob(row, search_cols)
        
        title_innov = any_match(self.title_innov_rd, title)
        innov_hits = count_unique_hits(self.innov_rd_strong, text)
        
        result["title_innov_rd"] = title_innov
        result["innov_signals_text"] = innov_hits
        
        if not (title_innov or innov_hits >= self.config.min_innov_signals_text):
            return result
        
        # 5) THEMES + POINTS
        total_theme_hits = 0
        theme_points = 0
        
        for theme, patterns in self.theme_patterns.items():
            hits = count_unique_hits(patterns, text)
            result[f"{theme} hits"] = hits
            total_theme_hits += hits
            
            if hits:
                theme_points += min(
                    hits * self.config.w_theme_hit + (self.config.w_theme_bonus if hits >= 2 else 0),
                    self.config.max_theme_points
                )
        
        result["theme_points"] = theme_points
        result["anti_function_title"] = any_match(self.anti_function, title)
        
        if total_theme_hits < self.config.min_theme_hits_total:
            return result
        
        # 5b) EXTRA: EVENT-ANGLE KEYWORDS IN TITLE
        title_event_points = 0
        if "Event Angle (Dynamic)" in self.theme_patterns:
            title_event_hits = count_unique_hits(self.theme_patterns["Event Angle (Dynamic)"], title)
            title_event_points = min(
                title_event_hits * self.config.w_title_event_hit,
                self.config.max_title_event_points
            )
        result["title_event_points"] = title_event_points
        
        # 6) FINAL SCORE
        score = 0
        score += title_event_points
        
        # VP and Director equal importance
        if is_vp or is_dir_innov:
            score += self.config.w_senior_top
        elif is_head:
            score += self.config.w_head
        
        score += (self.config.w_title_innov if title_innov else 0)
        score += (self.config.w_text_innov if innov_hits >= self.config.min_innov_signals_text else 0)
        score += theme_points
        
        if result["anti_function_title"] and not title_innov:
            score += self.config.penalty_anti_function
        
        result["total_score"] = score
        result["eligible"] = True
        return result
    
    def score_dataframe(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
        """
        Score all profiles in a DataFrame.
        
        Args:
            df: Input DataFrame with LinkedIn profiles
            
        Returns:
            Tuple of (all_eligible_sorted, top_n, stats)
        """
        # Process names
        df = process_names(df)
        
        # Get searchable columns
        search_cols = self._get_search_cols(df)
        col_title = pick_col(df, ["title"])
        
        # Score all rows
        scored = df.copy()
        score_df = scored.apply(
            lambda row: self._score_row(row, col_title, search_cols),
            axis=1,
            result_type="expand"
        )
        scored = pd.concat([scored, score_df], axis=1)
        
        # Filter and sort eligible profiles
        scored_sorted = (
            scored[scored["eligible"] == True]
            .sort_values("total_score", ascending=False)
            .reset_index(drop=True)
        )
        
        # Get top N
        top = scored_sorted.head(self.config.top_n).copy()
        
        # Compute stats
        stats = {
            "total_profiles": len(df),
            "eligible_profiles": len(scored_sorted),
            "top_n": len(top),
            "event_topic": self.event_topic,
            "dynamic_keywords": self.dynamic_keywords,
            "themes": list(self.theme_patterns.keys()),
        }
        
        if len(top) > 0:
            not_ok = top[~top["company_ok"]]
            stats["top_n_company_failures"] = len(not_ok)
        else:
            stats["top_n_company_failures"] = 0
        
        return scored_sorted, top, stats
    
    def export_to_excel(self, scored_sorted: pd.DataFrame, top: pd.DataFrame) -> bytes:
        """
        Export scored profiles to Excel format.
        
        Returns:
            Excel file as bytes
        """
        import io
        
        scored_sorted_clean = sanitize_for_excel(scored_sorted)
        top_clean = sanitize_for_excel(top)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            scored_sorted_clean.to_excel(writer, index=False, sheet_name="Eligible Ranked")
            top_clean.to_excel(writer, index=False, sheet_name=f"Top {self.config.top_n}")
        
        output.seek(0)
        return output.getvalue()
