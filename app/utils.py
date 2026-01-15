"""Utility functions for name cleaning, company matching, and text processing."""

from __future__ import annotations

import re
import unicodedata
from typing import Tuple, List, Optional

import pandas as pd


# Tokens to remove from names
REMOVE_TOKENS = [
    r"\bprof\.?\b", r"\bdr\.?\b", r"\bdott\.?\b", r"\bdipl\.?\b", r"\bing\.?\b", r"\bmed\.?\b",
    r"\bph\.?d\.?\b", r"\bmba\b", r"\bemba\b", r"\bmsc\b", r"\bm\.?sc\.?\b", r"\bbsc\b", r"\bma\b",
    r"\bll\.?m\.?\b", r"\bb\.?eng\.?\b",
    r"\bcfa\b", r"\bcpa\b", r"\bacca\b", r"\bcima\b", r"\bcgma\b", r"\bfrm\b", r"\bpmp\b",
    r"\bprince2\b", r"\bitil\b", r"\bcissp\b",
    r"\bjr\.?\b", r"\bsr\.?\b", r"\bsenior\b", r"\bjunior\b",
    r"\bassociate\b", r"\bassoc\.?\b", r"\bchartered\b",
    r"\bexecutive\b", r"\brealtor\b",
    r"\bii\b", r"\biii\b", r"\biv\b",
]

SYMBOLS_PATTERN = r"[~ª©¤+°·•®™¦_*()\[\]{}<>\"""''&|/\\\-–—]"
TOKENS_RE = re.compile("|".join(REMOVE_TOKENS), flags=re.IGNORECASE)
MULTI_SPACE_RE = re.compile(r"\s{2,}")

# Excel illegal characters pattern
ILLEGAL_XL_CHARS = re.compile(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]")


def clean_full_name(name: str) -> str:
    """Clean a full name by removing titles, symbols, and extra whitespace."""
    if pd.isna(name):
        return name
    s = str(name)
    s = re.sub(SYMBOLS_PATTERN, " ", s)
    s = re.sub(TOKENS_RE, " ", s)
    s = re.sub(r"-\s*ing\b", " ", s, flags=re.IGNORECASE)
    s = re.sub(r"[.,;:]", " ", s)
    s = MULTI_SPACE_RE.sub(" ", s).strip()
    return s


def to_ascii(s: str) -> str:
    """Convert a string to ASCII, handling special characters."""
    if pd.isna(s):
        return s
    s = str(s)
    s_norm = unicodedata.normalize("NFKD", s)
    s_no_marks = "".join(ch for ch in s_norm if not unicodedata.combining(ch))
    special_map = str.maketrans({
        "ß": "ss", "Þ": "Th", "þ": "th",
        "Đ": "D", "đ": "d",
        "Ł": "L", "ł": "l",
        "Æ": "AE", "æ": "ae",
        "Œ": "OE", "œ": "oe",
        "Ø": "O", "ø": "o",
        "Å": "A", "å": "a",
        "İ": "I", "ı": "i",
        "Ğ": "G", "ğ": "g",
        "Ş": "S", "ş": "s",
        "Č": "C", "č": "c",
        "Ć": "C", "ć": "c",
        "Š": "S", "š": "s",
        "Ž": "Z", "ž": "z",
        "Ś": "S", "ś": "s",
        "Ź": "Z", "ź": "z",
        "Ż": "Z", "ż": "z",
        "Ș": "S", "ș": "s",
        "Ț": "T", "ț": "t",
        "Ť": "T", "ť": "t",
        "Ď": "D", "ď": "d",
        "Ľ": "L", "ľ": "l",
        "Ř": "R", "ř": "r",
        "Ç": "C", "ç": "c",
        "Ñ": "N", "ñ": "n",
    })
    s_ascii = s_no_marks.translate(special_map)
    s_ascii = " ".join(s_ascii.split()).strip()
    return s_ascii


def normalize_company(s: str) -> str:
    """Normalize a company name for matching."""
    return (
        str(s or "")
        .lower()
        .replace("&", "and")
        .replace(".", "")
        .replace(",", "")
        .strip()
    )


class CompanyMatcher:
    """Class for matching company names against an allowlist."""
    
    def __init__(self, allowed_companies: list[str], company_variants: dict[str, list[str]]):
        """Initialize the company matcher with allowlist and variants."""
        self.allowed_canon_norm = {
            normalize_company(c): c for c in allowed_companies
        }
        
        self.variant_to_canon = {}
        for canon, variants in company_variants.items():
            for v in variants:
                self.variant_to_canon[normalize_company(v)] = canon
            self.variant_to_canon[normalize_company(canon)] = canon
    
    def match(self, company_name: str) -> Tuple[bool, str, str]:
        """
        Match a company name against the allowlist.
        
        Returns:
            Tuple of (is_allowed, canonical_name, match_reason)
        """
        c_norm = normalize_company(company_name)
        
        if c_norm in self.allowed_canon_norm:
            return True, self.allowed_canon_norm[c_norm], "direct_canonical"
        
        if c_norm in self.variant_to_canon:
            canon = self.variant_to_canon[c_norm]
            if normalize_company(canon) in self.allowed_canon_norm:
                return True, canon, "variant_match"
        
        return False, "", "not_allowed"


def safe_text(x) -> str:
    """Convert a value to a safe string, handling NaN."""
    if pd.isna(x):
        return ""
    return str(x)


def cregex(patterns: list[str]) -> list[re.Pattern]:
    """Compile a list of regex patterns with case-insensitive flag."""
    return [re.compile(p, flags=re.IGNORECASE) for p in patterns]


def any_match(patterns: list[re.Pattern], text: str) -> bool:
    """Check if any pattern matches the text."""
    return any(p.search(text) for p in patterns)


def count_unique_hits(patterns: list[re.Pattern], text: str) -> int:
    """Count the number of unique pattern hits in the text."""
    return sum(1 for p in patterns if p.search(text))


def pick_col(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """Pick the first matching column from a list of candidates."""
    cols = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        key = cand.lower().strip()
        if key in cols:
            return cols[key]
    return None


def sanitize_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """Remove Excel-illegal control characters from a DataFrame."""
    import numpy as np
    
    df2 = df.copy()
    obj_cols = df2.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        df2[c] = (
            df2[c]
            .astype(str)
            .map(lambda s: ILLEGAL_XL_CHARS.sub("", s))
            .map(lambda s: s.replace("\u00ad", ""))  # soft hyphen
        )
        df2.loc[df[c].isna(), c] = np.nan
    return df2


def _clean_csv_content(raw_bytes: bytes) -> bytes:
    """
    Clean problematic characters from CSV content.
    
    Removes control characters and normalizes line endings that can cause
    parser errors (especially with LinkedIn Sales Navigator exports).
    """
    # Remove problematic control characters
    # 0x02 = STX (Start of Text), 0x0B = VT (Vertical Tab)
    cleaned = raw_bytes.replace(b'\x02', b'').replace(b'\x0b', b'')
    
    # Normalize line endings to LF
    cleaned = cleaned.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    
    return cleaned


def load_data_file(uploaded_file) -> Tuple[pd.DataFrame, str]:
    """
    Load a CSV or Excel file into a DataFrame.
    
    Automatically cleans problematic characters from CSV files.
    
    Returns:
        Tuple of (DataFrame, event_topic_from_cell_a1)
    """
    from io import BytesIO
    
    filename = uploaded_file.name.lower()
    
    if filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
        # Read Excel cell A1 (first sheet) for dynamic topic
        uploaded_file.seek(0)
        _raw = pd.read_excel(uploaded_file, sheet_name=0, header=None)
        event_topic_from_cell = str(_raw.iat[0, 0]) if _raw.size else ""
    else:
        # Read raw bytes and clean problematic characters
        raw_bytes = uploaded_file.read()
        cleaned_bytes = _clean_csv_content(raw_bytes)
        cleaned_file = BytesIO(cleaned_bytes)
        
        # Try fast C parser first, fall back to Python parser if needed
        try:
            df = pd.read_csv(cleaned_file)
        except Exception:
            cleaned_file.seek(0)
            df = pd.read_csv(cleaned_file, engine='python')
        
        event_topic_from_cell = ""  # CSV has no "cell A1"
    
    return df, event_topic_from_cell


def process_names(df: pd.DataFrame) -> pd.DataFrame:
    """Process the fullName column to create cleaned versions."""
    if "fullName" not in df.columns:
        raise ValueError("Column 'fullName' not found in dataset.")
    
    df = df.copy()
    df["fullName_original"] = df["fullName"]
    df["fullName"] = df["fullName"].apply(clean_full_name)
    df["fullName_ascii"] = df["fullName"].apply(to_ascii)
    df["fullName_export"] = df["fullName_ascii"]
    
    return df
