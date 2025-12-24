import pandas as pd
from config import NODES_FILE, EDGES_FILE
from parse_profiles import load_all_agents
from parse_interactions import parse_all_interactions
from logger import get_logger

# Logging setup
logger = get_logger(__name__)


def build_nodes_and_edges():
    agent_users = load_all_agents()
    users, edges = parse_all_interactions()

    # Ensure agent ground truth overrides everything
    for user_id, info in agent_users.items():
        users[user_id] = info

    nodes_df = pd.DataFrame(users.values()).drop_duplicates("user_id")
    nodes_df["is_agent"] = nodes_df["is_agent"].fillna(False)

    edges_df = pd.DataFrame(edges)

    return nodes_df, edges_df

def save_nodes_and_edges(nodes_df, edges_df):
    nodes_df.to_csv(NODES_FILE, index=False)
    edges_df.to_csv(EDGES_FILE, index=False)

if __name__ == "__main__":
    logger.info("Starting node and edge construction")

    nodes, edges = build_nodes_and_edges()
    save_nodes_and_edges(nodes, edges)

    logger.info(f"Saved {len(nodes)} nodes to {NODES_FILE}")
    logger.info(f"Saved {len(edges)} edges to {EDGES_FILE}")
    logger.info("Pipeline completed successfully")

