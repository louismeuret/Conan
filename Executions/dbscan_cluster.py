import pandas as pd
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

#print(sys.argv[1])
def dbscan_clust(results):

    finallist = []
    for x in results:
        if len(x) == 6:
            finallist.append([x[0],x[5][0],x[5][1],x[5][2],x[1]])
        else:
            finallist.append([x[0],x[7][0],x[7][1],x[7][2],x[1]])


    df = pd.DataFrame(finallist,columns=['Name','X','Y','Z','Colours'])
    data = df[['X','Y','Z']]
    print(data)

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # Create an instance of the DBSCAN algorithm
    dbscan = DBSCAN(eps=0.5, min_samples=5)

    # Fit the DBSCAN model to the scaled data
    dbscan.fit(data_scaled)

    # Add the cluster labels to the original dataframe
    data['Cluster'] = dbscan.labels_
    return data