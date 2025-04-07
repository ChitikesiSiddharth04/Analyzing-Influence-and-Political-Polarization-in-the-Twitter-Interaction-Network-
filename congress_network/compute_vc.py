# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:39:37 2022

@author: finkt
"""
import sys
import os
import warnings
warnings.filterwarnings('ignore')  # Suppress the runtime warning

from viral_centrality import viral_centrality
import json
import numpy as np
from matplotlib import pyplot as plt

# Set parameters
tol = 0.001
beta = 1.0  # Transmission probability scaling factor

# Load data
print("Loading network data...")
f = open('congress_network_data.json')
data = json.load(f)

inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

print("Computing viral centrality...")
num_activated = viral_centrality(inList, inWeight, outList, Niter = -1, beta = beta, tol = tol)

# Sort results
sorted_indices = np.argsort(num_activated)[::-1]  # Descending order
sorted_scores = num_activated[sorted_indices]
sorted_usernames = [usernameList[i] for i in sorted_indices]

# Create visualization
plt.figure(figsize=(12, 6))
plt.scatter(np.array(range(len(num_activated))), num_activated, color='red', label='Viral Centrality')
plt.xlabel('Node ID', fontsize=15)
plt.ylabel('Average Number Activated', fontsize=15)
plt.title('Viral Centrality Scores for Congressional Twitter Network', fontsize=16)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot
plt.savefig('viral_centrality_results.png')
print("Results saved to viral_centrality_results.png")

# Print top 10 most influential members
print("\nTop 10 Most Influential Congress Members:")
for i in range(min(10, len(sorted_usernames))):
    print(f"{i+1}. @{sorted_usernames[i]}: {sorted_scores[i]:.2f}")

