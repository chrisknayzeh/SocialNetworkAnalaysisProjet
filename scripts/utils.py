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