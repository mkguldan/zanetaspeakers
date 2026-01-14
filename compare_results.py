"""Compare original and new tool results."""
import pandas as pd
import numpy as np

orig = pd.read_excel('results_original.xlsx', sheet_name=0)
new = pd.read_excel('results_newtool.xlsx', sheet_name='Eligible Ranked')

print(f'Original: {len(orig)} profiles')
print(f'New tool: {len(new)} profiles')

# Use linkedInProfileUrl as identifier
orig['_id'] = orig['linkedInProfileUrl'].astype(str).str.strip()
new['_id'] = new['linkedInProfileUrl'].astype(str).str.strip()

# Find common profiles
orig_ids = set(orig['_id'].dropna())
new_ids = set(new['_id'].dropna())

common = orig_ids & new_ids
only_orig = orig_ids - new_ids
only_new = new_ids - orig_ids

print(f'\nProfiles in both: {len(common)}')
print(f'Only in original: {len(only_orig)}')
print(f'Only in new: {len(only_new)}')

if only_orig:
    print(f'\n  Examples only in original (first 3):')
    for x in list(only_orig)[:3]:
        row = orig[orig['_id']==x].iloc[0]
        print(f'    {row.get("fullName_export", "?")} @ {row.get("companyName", "?")}')

if only_new:
    print(f'\n  Examples only in new (first 3):')
    for x in list(only_new)[:3]:
        row = new[new['_id']==x].iloc[0]
        print(f'    {row.get("fullName_export", "?")} @ {row.get("companyName", "?")}')

# Compare scoring columns for common profiles
print('\n=== Comparing Scores for Common Profiles ===')
scoring_cols = ['total_score', 'eligible', 'company_ok', 'is_vp', 'is_dir_innov', 'is_head', 
                'is_senior', 'title_innov_rd', 'innov_signals_text', 'theme_points', 
                'title_event_points', 'title_disqualified', 'anti_function_title']

# Merge on ID
merged = orig[['_id'] + [c for c in scoring_cols if c in orig.columns]].merge(
    new[['_id'] + [c for c in scoring_cols if c in new.columns]], 
    on='_id', 
    suffixes=('_orig', '_new')
)

print(f'Merged profiles: {len(merged)}')

all_match = True
for col in scoring_cols:
    if f'{col}_orig' in merged.columns and f'{col}_new' in merged.columns:
        orig_vals = merged[f'{col}_orig']
        new_vals = merged[f'{col}_new']
        
        # Handle NaN comparison
        both_nan = orig_vals.isna() & new_vals.isna()
        both_equal = (orig_vals == new_vals) | both_nan
        
        matches = both_equal.sum()
        mismatches = len(merged) - matches
        
        if mismatches == 0:
            print(f'  OK {col}: All {matches} values match')
        else:
            all_match = False
            print(f'  XX {col}: {mismatches} mismatches')
            # Show first few mismatches
            mismatch_rows = merged[~both_equal].head(3)
            for _, row in mismatch_rows.iterrows():
                print(f'      orig={row[f"{col}_orig"]}, new={row[f"{col}_new"]}')

# Also compare theme hit columns
print('\n=== Comparing Theme Hits ===')
theme_cols = [c for c in orig.columns if 'hits' in c.lower()]
for col in theme_cols:
    if col in orig.columns and col in new.columns:
        merged2 = orig[['_id', col]].merge(new[['_id', col]], on='_id', suffixes=('_orig', '_new'))
        orig_vals = merged2[f'{col}_orig'].fillna(0)
        new_vals = merged2[f'{col}_new'].fillna(0)
        
        matches = (orig_vals == new_vals).sum()
        mismatches = len(merged2) - matches
        
        if mismatches == 0:
            print(f'  OK {col}: All match')
        else:
            all_match = False
            print(f'  XX {col}: {mismatches} mismatches')

print('\n' + '='*50)
if all_match and len(only_orig) == 0 and len(only_new) == 0:
    print('RESULT: All scores match exactly!')
else:
    print('RESULT: Differences found (see above)')
