import json
from datetime import datetime
from config import TWEETS_DIR, MENTIONS_DIR
from logger import get_logger

# Logging setup
logger = get_logger(__name__)


def parse_twitter_date(date_str):
    try:
      return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    except ValueError as e:
        logger.warning(f"Date parsing error for '{date_str}': {e}")
        return None

def extract_edges_from_tweet(tweet, users):
    edges = []

    author = tweet["author"]
    source_id = author["id"]

    users[source_id] = {
        "user_id": source_id,
        "username": author["userName"],
        "is_agent": author.get("isAutomated", False)
    }

    created_at = parse_twitter_date(tweet["createdAt"])

    mentions = tweet.get("entities", {}).get("user_mentions", [])

    for m in mentions:
        target_id = m["id_str"]

        users[target_id] = {
            "user_id": target_id,
            "username": m["screen_name"],
            "is_agent": False  # fixed later
        }

        edges.append({
            "source_id": source_id,
            "target_id": target_id,
            "timestamp": created_at,
            "tweet_id": tweet["id"],
            "type": "mention"
        })

    return edges

def parse_folder(folder, users):
    edges = []

    logger.info(f"Parsing folder: {folder.name}")

    for file in folder.glob("*.json"):
        logger.info(f"Processing file: {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tweets = data.get("tweets", [])
        logger.info(f"Found {len(tweets)} tweets in {file.name}")

        for tweet in tweets:
            edges.extend(extract_edges_from_tweet(tweet, users))

    logger.info(f"Extracted {len(edges)} edges from {folder.name}")
    return edges


def parse_all_interactions():
    users = {}
    edges = []

    edges.extend(parse_folder(TWEETS_DIR, users))
    edges.extend(parse_folder(MENTIONS_DIR, users))

    return users, edges
