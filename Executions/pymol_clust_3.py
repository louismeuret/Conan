import pandas as pd
import pymol
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib 

# Read the pickled DataFrame
unpickled_df = pd.read_pickle("../parametres/temp_files/list_results.pkl")

# Create a new DataFrame with selected columns
new_df = pd.DataFrame(unpickled_df, columns=['lig', 'Energy', 'logp', 'molwt', 'complexity', 'coord'])
new_df = new_df[new_df['logp'] != 0]

# Extract coordinates for clustering
coordinates = np.array(new_df['coord'].tolist())

# Perform DBSCAN clustering
eps = 3.0  # Adjust the epsilon value based on your data
min_samples = 5  # Adjust the minimum number of samples based on your data
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
new_df['cluster'] = dbscan.fit_predict(coordinates)

# Launch PyMOL
pymol.finish_launching()

# Get the unique clusters
unique_clusters = new_df['cluster'].unique()

# Transform negative cluster indices into positive values for normalization
norm_clusters = matplotlib.colors.Normalize(vmin=min(unique_clusters), vmax=max(unique_clusters) + 1)

# Loop through the DataFrame and visualize atoms in PyMOL with different colors for each cluster
for index, row in new_df.iterrows():
    name = row['lig'].replace(":", "")
    x, y, z = row['coord']
    energy = row['Energy']

    # Get the cluster color based on the normalized cluster value
    cluster_color = matplotlib.cm.get_cmap('tab10')(norm_clusters(row['cluster']))

    r, g, b, _ = cluster_color

    # Create a pseudoatom with a specific name and position
    pymol.cmd.pseudoatom(name, pos=[x, y, z])

    # Set the color for the pseudoatom
    pymol.cmd.set_color('point_color', [r, g, b])

    # Color the pseudoatom
    pymol.cmd.color('point_color', name)

    # Show the spheres for the pseudoatom
    pymol.cmd.show('spheres', name)

# Save the clustered DataFrame to a pickle file
new_df.to_pickle("../parametres/temp_files/clustered_results.pkl")

