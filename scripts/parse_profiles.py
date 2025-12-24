import json
import pandas as pd
from config import PROFILES_DIR, COOKIE_LIST, DELIMITER
from logger import get_logger

# Logging setup
logger = get_logger(__name__)

def load_agents_from_profiles():
    agents = {}
    skipped = 0

    for file in PROFILES_DIR.glob("*.json"):
        logger.info(f"Reading profile: {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if raw is None:
            logger.warning(f"Profile {file.name} is null — skipped")
            skipped += 1
            continue

        data = raw.get("data") if isinstance(raw, dict) else raw

        if data is None:
            logger.warning(f"No data in profile {file.name} — skipped")
            skipped += 1
            continue

        if isinstance(data, list):
            if len(data) == 0:
                logger.warning(f"Empty data list in {file.name}")
                skipped += 1
                continue
            data = data[0]

        if not isinstance(data, dict):
            logger.warning(f"Unexpected structure in {file.name}")
            skipped += 1
            continue

        user_id = data.get("id")
        username = data.get("userName")

        if user_id is None:
            logger.warning(f"Missing user_id in {file.name}")
            skipped += 1
            continue

        agents[user_id] = {
            "user_id": user_id,
            "username": username,
            "is_agent": True
        }

        logger.info(f"Loaded agent profile: {username} ({user_id})")

    logger.info(f"Loaded {len(agents)} agent profiles, skipped {skipped}")
    return agents


def load_agents_from_cookie_list():
    agents = {}

    df = pd.read_csv(COOKIE_LIST, delimiter=DELIMITER)

    # Adjust column names here if needed
    for _, row in df.iterrows():
        user_id = str(row.get("twitter_id"))
        username = row.get("twitter_handle")

        if pd.notna(user_id):
            agents[user_id] = {
                "user_id": user_id,
                "username": username,
                "is_agent": True
            }

    return agents

def load_all_agents():
    agents = load_agents_from_profiles()
    agents.update(load_agents_from_cookie_list())
    return agents
