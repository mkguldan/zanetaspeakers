"""Check what config the original might have used."""
import pandas as pd

# Check input.csv for any topic info
try:
    # Check if Excel and has A1 topic
    df = pd.read_csv('input.csv', nrows=1, header=None)
    print("Input CSV first cell A1:", df.iat[0,0] if df.size else "empty")
except:
    pass

# Check original results for clues
orig = pd.read_excel('results_original.xlsx', sheet_name=0)

# The EVENT_TOPIC in config.py is:
default_topic = "Internal and External Startups & Ecosystems & Partnerships & Ventures"
print(f"\nDefault EVENT_TOPIC_OVERRIDE: {default_topic}")

# Check which keyword packs would match
TOPIC_KEYWORD_PACKS = {
    "collaboration": ["culture", "capability building", "learning", "leadership", 
                      "change management", "psychological safety", "trust", "talent",
                      "org design", "operating model"],
    "ai": ["ai", "artificial intelligence", "generative ai", "genai", "llm",
           "machine learning", "data", "analytics"],
    "business model": ["business model", "new business", "growth", "venture", "venturing",
                       "incubator", "accelerator", "corporate venture", "portfolio"],
    "sustain": ["sustainability", "circular", "circularity", "net zero", "decarbon", "climate", "esg"],
}

topic_lower = default_topic.lower()
print(f"\nChecking which keyword packs match '{default_topic}':")
for key, kws in TOPIC_KEYWORD_PACKS.items():
    matches = key.lower() in topic_lower
    print(f"  '{key}' in topic: {matches}")

# Check what dynamic keywords would exist based on the topic
print("\n--- If we add more keyword pack keys ---")
# The original file has Event Angle (Dynamic) hits with non-zero values
# This means some keyword pack DID match. Let's see what topics WOULD match.

possible_topics_that_could_match = [
    "Internal and External Startups & Ecosystems & Partnerships & Ventures",  # default
    "AI and Innovation",
    "Sustainability and Innovation", 
    "Business Model Innovation",
    "Collaboration and Culture",
]

for topic in possible_topics_that_could_match:
    t_lower = topic.lower()
    matched = [k for k in TOPIC_KEYWORD_PACKS.keys() if k.lower() in t_lower]
    if matched:
        print(f"  '{topic}' -> matches: {matched}")

# The original must have used a different EVENT_TOPIC
# Let's check column names for hints
print("\n=== Original columns that might indicate config ===")
for col in orig.columns:
    if 'event' in col.lower() or 'topic' in col.lower() or 'angle' in col.lower():
        print(f"  {col}")
