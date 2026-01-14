"""Debug the scoring differences."""
import pandas as pd

orig = pd.read_excel('results_original.xlsx', sheet_name=0)
new = pd.read_excel('results_newtool.xlsx', sheet_name='Eligible Ranked')

# Check for Event Angle column
print("=== Checking Event Angle (Dynamic) ===")
event_col = 'Event Angle (Dynamic) hits'
if event_col in orig.columns:
    print(f"Original has '{event_col}': YES")
    print(f"  Non-zero values: {(orig[event_col].fillna(0) > 0).sum()}")
    print(f"  Sample values: {orig[event_col].head(10).tolist()}")
else:
    print(f"Original has '{event_col}': NO")

if event_col in new.columns:
    print(f"New tool has '{event_col}': YES")
    print(f"  Non-zero values: {(new[event_col].fillna(0) > 0).sum()}")
else:
    print(f"New tool has '{event_col}': NO")

# Compare theme_points calculation
print("\n=== Theme Points Calculation Check ===")
theme_cols = [
    'Gamechanging Innovation hits',
    'New Business Models & Foresight hits', 
    'Culture & Leadership for Innovation & Agility hits',
    'Digital Innovation & Transformation hits',
    'AI & Generative AI, Data & IoT hits',
    'Customer Centricity, Front End & Design Thinking hits',
    'Innovation for Sustainability, Circularity & Net Zero hits',
    'Startup Collaboration, Open Innovation & Ecosystems hits',
    'Managing, Measuring & Accelerating R&D hits'
]

# Check first profile
orig['_id'] = orig['linkedInProfileUrl'].astype(str).str.strip()
new['_id'] = new['linkedInProfileUrl'].astype(str).str.strip()

common_id = new['_id'].iloc[0]
orig_row = orig[orig['_id'] == common_id].iloc[0]
new_row = new[new['_id'] == common_id].iloc[0]

print(f"\nProfile: {orig_row.get('fullName_export', '?')}")
print(f"\nTheme hits comparison:")

W_THEME_HIT = 3
W_THEME_BONUS = 6
MAX_THEME_POINTS = 30

orig_calc_theme = 0
new_calc_theme = 0

for col in theme_cols:
    if col in orig.columns and col in new.columns:
        o = orig_row[col]
        n = new_row[col]
        print(f"  {col}: orig={o}, new={n}")
        
        # Calculate expected points
        if o > 0:
            pts = min(o * W_THEME_HIT + (W_THEME_BONUS if o >= 2 else 0), MAX_THEME_POINTS)
            orig_calc_theme += pts
        if n > 0:
            pts = min(n * W_THEME_HIT + (W_THEME_BONUS if n >= 2 else 0), MAX_THEME_POINTS)
            new_calc_theme += pts

# Check Event Angle Dynamic
if event_col in orig.columns:
    o = orig_row[event_col] if not pd.isna(orig_row[event_col]) else 0
    print(f"  {event_col}: orig={o}")
    if o > 0:
        pts = min(o * W_THEME_HIT + (W_THEME_BONUS if o >= 2 else 0), MAX_THEME_POINTS)
        orig_calc_theme += pts

print(f"\nCalculated theme_points from hits:")
print(f"  Original calculated: {orig_calc_theme}")
print(f"  New calculated: {new_calc_theme}")
print(f"  Original actual: {orig_row['theme_points']}")
print(f"  New actual: {new_row['theme_points']}")

print(f"\ntitle_event_points:")
print(f"  Original: {orig_row['title_event_points']}")
print(f"  New: {new_row['title_event_points']}")

print(f"\ntotal_score:")
print(f"  Original: {orig_row['total_score']}")
print(f"  New: {new_row['total_score']}")
