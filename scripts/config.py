from pathlib import Path

# Root directories
RAW_DATA = Path("data/raw")
PROCESSED_DATA = Path("data/processed")

# Raw data folders
PROFILES_DIR = RAW_DATA / "profiles"
TWEETS_DIR = RAW_DATA / "tweets"
MENTIONS_DIR = RAW_DATA / "mentions"
COOKIE_LIST = RAW_DATA / "OriginalListCookie.fun.csv"
DELIMITER = ";"

# Processed outputs
NODES_FILE = PROCESSED_DATA / "nodes.csv"
EDGES_FILE = PROCESSED_DATA / "edges.csv"
TWEETS_FILE = PROCESSED_DATA / "tweets.csv"

# Ensure processed directory exists
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
