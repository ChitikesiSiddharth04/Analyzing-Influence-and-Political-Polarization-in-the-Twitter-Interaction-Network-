import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# Load data
print("Loading network data...")
f = open('congress_network_data.json')
data = json.load(f)

inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

# Create directed graph
print("Creating network graph...")
G = nx.DiGraph()

# Add nodes
for i, username in enumerate(usernameList):
    G.add_node(i, username=username)

# Add edges with weights
for i in range(len(outList)):
    for j, target in enumerate(outList[i]):
        weight = outWeight[i][j]
        G.add_edge(i, target, weight=weight)

# Calculate different centrality measures
print("\nCalculating centrality measures...")

# 1. Degree Centrality
degree_centrality = nx.degree_centrality(G)
in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)

# 2. Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

# 3. Closeness Centrality
closeness_centrality = nx.closeness_centrality(G)

# 4. Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)

# 5. PageRank
pagerank = nx.pagerank(G, weight='weight')

# Combine all measures
all_measures = {
    'Degree': degree_centrality,
    'In-Degree': in_degree_centrality,
    'Out-Degree': out_degree_centrality,
    'Betweenness': betweenness_centrality,
    'Closeness': closeness_centrality,
    'Eigenvector': eigenvector_centrality,
    'PageRank': pagerank
}

# Function to get top N members for each measure
def get_top_members(measure_dict, n=10):
    sorted_items = sorted(measure_dict.items(), key=lambda x: x[1], reverse=True)
    return [(usernameList[i], score) for i, score in sorted_items[:n]]

# Print results for each measure
print("\nTop 10 Most Influential Members by Different Measures:")
for measure_name, measure_dict in all_measures.items():
    print(f"\n{measure_name} Centrality:")
    top_members = get_top_members(measure_dict)
    for i, (username, score) in enumerate(top_members, 1):
        print(f"{i}. @{username}: {score:.4f}")

# Create a combined influence score
print("\nCalculating combined influence score...")
combined_scores = defaultdict(float)
for measure_dict in all_measures.values():
    for node, score in measure_dict.items():
        combined_scores[node] += score

# Normalize combined scores
max_score = max(combined_scores.values())
combined_scores = {k: v/max_score for k, v in combined_scores.items()}

# Get top members by combined score
print("\nTop 10 Most Influential Members (Combined Score):")
top_combined = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (node, score) in enumerate(top_combined, 1):
    print(f"{i}. @{usernameList[node]}: {score:.4f}")

# Visualization
plt.figure(figsize=(15, 10))

# Create subplots for each measure
n_measures = len(all_measures)
n_cols = 3
n_rows = (n_measures + n_cols - 1) // n_cols

for idx, (measure_name, measure_dict) in enumerate(all_measures.items()):
    plt.subplot(n_rows, n_cols, idx + 1)
    
    # Get top 10 scores
    top_scores = sorted(measure_dict.values(), reverse=True)[:10]
    top_members = [usernameList[i] for i, _ in sorted(measure_dict.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    # Create bar plot
    plt.bar(range(len(top_scores)), top_scores, color='skyblue')
    plt.xticks(range(len(top_scores)), [f"@{name}" for name in top_members], rotation=45, ha='right')
    plt.title(f'{measure_name} Centrality')
    plt.tight_layout()

plt.suptitle('Top 10 Members by Different Centrality Measures', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('centrality_measures.png', dpi=300, bbox_inches='tight')
print("\nCentrality measures visualization saved to centrality_measures.png")

# Save results to file
with open('centrality_results.txt', 'w') as f:
    f.write("Top 10 Most Influential Members by Different Measures:\n\n")
    for measure_name, measure_dict in all_measures.items():
        f.write(f"{measure_name} Centrality:\n")
        top_members = get_top_members(measure_dict)
        for i, (username, score) in enumerate(top_members, 1):
            f.write(f"{i}. @{username}: {score:.4f}\n")
        f.write("\n")
    
    f.write("\nTop 10 Most Influential Members (Combined Score):\n")
    for i, (node, score) in enumerate(top_combined, 1):
        f.write(f"{i}. @{usernameList[node]}: {score:.4f}\n")

print("\nDetailed results saved to centrality_results.txt") 