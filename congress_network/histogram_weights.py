# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:41:58 2023

@author: finkt
"""

import json
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import lognorm

# Load data
print("Loading network data...")
f = open('congress_network_data.json')
data = json.load(f)

# Extract all weights
all_weights = []
for weights in data[0]['inWeight']:
    all_weights.extend(weights)
all_weights = np.array(all_weights)

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(all_weights, bins=50, color='blue', alpha=0.7, edgecolor='black')
plt.xlabel('Transmission Probability', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.title('Distribution of Transmission Probabilities in Congressional Twitter Network', fontsize=16)
plt.grid(True, alpha=0.3)

# Add statistics
mean_weight = np.mean(all_weights)
median_weight = np.median(all_weights)
plt.axvline(mean_weight, color='red', linestyle='--', label=f'Mean: {mean_weight:.3f}')
plt.axvline(median_weight, color='green', linestyle='--', label=f'Median: {median_weight:.3f}')
plt.legend()

plt.tight_layout()
plt.savefig('weight_distribution.png')
print("Weight distribution plot saved to weight_distribution.png")

# Print statistics
print("\nNetwork Weight Statistics:")
print(f"Total number of connections: {len(all_weights)}")
print(f"Mean transmission probability: {mean_weight:.4f}")
print(f"Median transmission probability: {median_weight:.4f}")
print(f"Minimum transmission probability: {np.min(all_weights):.4f}")
print(f"Maximum transmission probability: {np.max(all_weights):.4f}")

# best fit of data for lognorm distribution
s, loc, scale=lognorm.fit(all_weights,floc=0.0)

x=np.linspace(0,0.14,10000)
y=lognorm.pdf(x,s, loc=loc, scale=scale)
plt.plot(x,y,label='lognorm',linewidth=4)

plt.legend()