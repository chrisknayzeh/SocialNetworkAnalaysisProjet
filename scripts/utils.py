import numpy as np

# Generate graph statistics

def graph_stats(graph):
  import igraph as ig
  import numpy as np

  num_nodes = graph.vcount()
  num_edges = graph.ecount()

  num_agents = sum(graph.vs['is_agent'])
  num_humans = num_nodes - num_agents

  in_degrees = graph.indegree()
  out_degrees = graph.outdegree()

  q1_in = round(np.percentile(in_degrees,25), 2)
  q3_in = round(np.percentile(in_degrees,75),2)

  q1_out = round(np.percentile(out_degrees,25), 2)
  q3_out = round(np.percentile(out_degrees,75),2)

  print("===== GRAPH STATISTICS =====")
  print(f"Nodes: {num_nodes}")
  print(f"Edges (unique interactions): {num_edges}")
  print(f"Humans: {num_humans}")
  print(f"Agents: {num_agents}")

  print("\nIn-degree statistics:")
  print("  Mean:", round(np.mean(in_degrees), 2))
  print(f"  Q1:{q1_in}")
  print("  Median:", np.median(in_degrees))
  print(f"  Q3:{q3_in}" )
  print("  Max:", max(in_degrees))

  print("\nOut-degree statistics:")
  print("  Mean:", round(np.mean(out_degrees), 2))
  print(f"  Q1:{q1_out}")
  print("  Median:", np.median(out_degrees))
  print(f"  Q3:{q3_out}" )
  print("  Max:", max(out_degrees))

# describing engagement
def describe_engagement(df, label):
  print(f"\n===== {label} =====")
  print("Count:", len(df))
  print("Mean:", round(df['engagement_local'].mean(), 3))
  print("Median:", round(df['engagement_local'].median(), 3))
  print("Std:", round(df['engagement_local'].std(), 3))
  print("Max:", round(df['engagement_local'].max(), 3))

# Freeman Centralization on In-Degree
def freeman_in_degree_centralization(graph):
    in_deg = np.array(graph.indegree())
    n = graph.vcount()
    if n < 3:
        return np.nan
    return np.sum(in_deg.max() - in_deg) / ((n - 1) * (n - 2))

def community_louvain(graph):
# Convert directed graph to undirected for community detection
  G_undirected = graph.as_undirected(
      combine_edges=dict(weight="sum")
  )

  # Louvain community detection
  communities = G_undirected.community_multilevel(
      weights=G_undirected.es['weight']
  )
  return communities

def build_week_graph(graph, week_label, edge_list):
    df_week = edge_list[edge_list['week'] == week_label]

    users = set(df_week['source_id']).union(df_week['target_id'])
    vertex_ids = [i for i, v in enumerate(graph.vs['user_id']) if v in users]

    G_week = graph.subgraph(vertex_ids)
    return G_week
