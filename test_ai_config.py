"""Test scoring with AI event topic to match original results."""
import sys
sys.path.insert(0, 'app')

import pandas as pd
from config import ScoringConfig
from scoring import ScoringEngine

# Load input
df = pd.read_csv('input.csv')
print(f"Loaded {len(df)} profiles from input.csv")

# Create config with AI event topic (like the original)
config = ScoringConfig.get_default()
config.event_topic_override = "AI"  # This will match the "ai" keyword pack

print(f"\nUsing EVENT_TOPIC_OVERRIDE: '{config.event_topic_override}'")

# Run scoring
engine = ScoringEngine(config)
print(f"Dynamic keywords activated: {engine.dynamic_keywords}")
print(f"Themes: {list(engine.theme_patterns.keys())}")

scored_sorted, top, stats = engine.score_dataframe(df)

print(f"\nEligible profiles: {stats['eligible_profiles']}")

# Export to compare
scored_sorted.to_excel('results_newtool_ai.xlsx', index=False, sheet_name='Eligible Ranked')
print("Saved to results_newtool_ai.xlsx")

# Now compare with original
print("\n=== Comparing with Original ===")
orig = pd.read_excel('results_original.xlsx', sheet_name=0)

orig['_id'] = orig['linkedInProfileUrl'].astype(str).str.strip()
scored_sorted['_id'] = scored_sorted['linkedInProfileUrl'].astype(str).str.strip()

# Merge and compare
merged = orig[['_id', 'total_score', 'theme_points', 'title_event_points']].merge(
    scored_sorted[['_id', 'total_score', 'theme_points', 'title_event_points']], 
    on='_id', 
    suffixes=('_orig', '_new')
)

print(f"Profiles in both: {len(merged)}")

for col in ['total_score', 'theme_points', 'title_event_points']:
    matches = (merged[f'{col}_orig'] == merged[f'{col}_new']).sum()
    mismatches = len(merged) - matches
    if mismatches == 0:
        print(f"  OK {col}: All {matches} values match!")
    else:
        print(f"  XX {col}: {mismatches} mismatches")
        # Show sample
        diff = merged[merged[f'{col}_orig'] != merged[f'{col}_new']].head(3)
        for _, row in diff.iterrows():
            print(f"      orig={row[f'{col}_orig']}, new={row[f'{col}_new']}")
