import numpy as np
from tabulate import tabulate
with open('resultatsgnina.npy','rb') as f:
    lst = np.load(f,allow_pickle=True)

print(tabulate(lst, headers = ["Nom ligand","Logiciel","Affinité minimisée","RMSD minimisé","CNNscore","CNNaffinity"]))
