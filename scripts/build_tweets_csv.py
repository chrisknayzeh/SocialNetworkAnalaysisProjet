import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import TWEETS_DIR, MENTIONS_DIR, PROCESSED_DATA
from logger import get_logger

logger = get_logger(__name__)


def parse_twitter_date(date_str):
    try:
        return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    except Exception as e:
        logger.warning(f"Date parsing error for '{date_str}': {e}")
        return None


def extract_tweets_from_folder(folder):
    rows = []

    logger.info(f"Parsing tweets from folder: {folder}")

    for file in folder.glob("*.json"):
        logger.info(f"Reading file: {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tweets = data.get("tweets", [])

        for tweet in tweets:
            author = tweet.get("author", {})

            rows.append({
                "tweet_id": tweet.get("id"),
                "user_id": author.get("id"),
                "text": tweet.get("text"),
                "created_at": parse_twitter_date(tweet.get("createdAt")),
                "lang": tweet.get("lang"),
                "conversation_id": tweet.get("conversationId"),
                "is_reply": tweet.get("isReply"),
                "in_reply_to_user_id": tweet.get("inReplyToUserId")
            })

    return rows


def build_tweets_dataframe():
    all_rows = []

    all_rows.extend(extract_tweets_from_folder(TWEETS_DIR))
    all_rows.extend(extract_tweets_from_folder(MENTIONS_DIR))

    tweets_df = pd.DataFrame(all_rows)

    # Minimal cleaning
    tweets_df = tweets_df.dropna(subset=["tweet_id", "user_id", "text"])
    tweets_df = tweets_df.drop_duplicates(subset="tweet_id")

    tweets_df["tweet_id"] = tweets_df["tweet_id"].astype(str)
    tweets_df["user_id"] = tweets_df["user_id"].astype(str)

    return tweets_df


if __name__ == "__main__":
    logger.info("Building tweets.csv")

    tweets_df = build_tweets_dataframe()
    tweets_df.to_csv(f"{PROCESSED_DATA}/tweets.csv", index=False)

    logger.info(f"Saved {len(tweets_df)} tweets to tweets.csv")
