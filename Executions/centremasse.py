from __future__ import division
import numpy as np
def centremasse(bestligandcopy):
    bestx = []
    besty = []
    bestz = []
    with open(bestligandcopy, 'r+') as file:
                        # read a list of lines into data
        data = file.readlines()
    for x in range(len(data)):
        if data[x][0:4] == "ATOM" or data[x][0:6] == "HETATM":
            bestx.append(float(data[x][31:37]))
            besty.append(float(data[x][39:45]))
            bestz.append(float(data[x][47:53]))
        #print(good)
        #print(x)
        centrex = np.mean(bestx)
        centrey = np.mean(besty)
        centrez = np.mean(bestz)
    return centrex, centrey, centrez
