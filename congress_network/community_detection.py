import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain
import matplotlib.cm as cm

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

# Convert to undirected graph for community detection
G_undirected = G.to_undirected()

# Detect communities using Louvain method
print("Detecting communities...")
partition = community_louvain.best_partition(G_undirected)

# Get number of communities
num_communities = len(set(partition.values()))
print(f"\nFound {num_communities} communities")

# Calculate community sizes
community_sizes = {}
for node, community in partition.items():
    if community not in community_sizes:
        community_sizes[community] = 0
    community_sizes[community] += 1

# Print community statistics
print("\nCommunity Statistics:")
for comm_id, size in sorted(community_sizes.items(), key=lambda x: x[1], reverse=True):
    print(f"Community {comm_id}: {size} members")

# Get top members in each community
print("\nTop Members in Each Community:")
for comm_id in range(num_communities):
    community_members = [i for i, c in partition.items() if c == comm_id]
    print(f"\nCommunity {comm_id} (Size: {len(community_members)}):")
    
    # Calculate average degree for members in this community
    degrees = [G.degree(member) for member in community_members]
    avg_degree = np.mean(degrees)
    print(f"Average degree: {avg_degree:.2f}")
    
    # Print top 5 members by degree
    sorted_members = sorted(community_members, key=lambda x: G.degree(x), reverse=True)[:5]
    for member in sorted_members:
        print(f"@{usernameList[member]} (Degree: {G.degree(member)})")

# Visualization
plt.figure(figsize=(15, 10))

# Use spring layout for better visualization
pos = nx.spring_layout(G_undirected, k=0.3, iterations=50)

# Draw the graph
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G_undirected, pos, partition.keys(), node_size=40,
                      cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G_undirected, pos, alpha=0.2)

plt.title(f'Congressional Twitter Network Communities (Total: {num_communities})', fontsize=16)
plt.axis('off')

# Save the plot
plt.savefig('community_detection.png', dpi=300, bbox_inches='tight')
print("\nCommunity visualization saved to community_detection.png")

# Calculate and print modularity
modularity = community_louvain.modularity(partition, G_undirected)
print(f"\nNetwork Modularity: {modularity:.4f}")
print("(Higher modularity indicates stronger community structure)") 