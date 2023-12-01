import pandas as pd
import pickle
listligand = pickle.load(open("listligand.pickle", "rb"))
print(listligand)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.DataFrame(listligand,columns=['Name','X','Y','Z','Colours'])
data = df[['X','Y','Z']]
print(data)
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Create an instance of the DBSCAN algorithm
dbscan = DBSCAN(eps=0.5, min_samples=5)

# Fit the DBSCAN model to the scaled data
dbscan.fit(data_scaled)

# Add the cluster labels to the original dataframe
data['Cluster'] = dbscan.labels_
print(data)
# Print the number of clusters found by the algorithm
n_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
print(f"Number of clusters found: {n_clusters}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(data['X'], data['Y'], data['Z'], c=data['Cluster'], cmap='viridis')
ax.set_title('DBSCAN Clustering')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
def on_click(event):
    if event.button == 1:  # Only do this on left-clicks
        x, y = event.xdata, event.ydata
        sel = scatter.contains(event)[0]
        print(sel)
        if sel:
            ind = np.nonzero(sel)[0]
            xs, ys, zs = scatter._offsets[ind].T[:3]
            dists = np.sqrt((xs - x) ** 2 + (ys - y) ** 2 + (zs - event.zdata) ** 2)
            ind = ind[np.argmin(dists)]
            label = df['Name'][ind]
            ax.text(xs[ind], ys[ind], zs[ind], label)

fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
plt.show()
