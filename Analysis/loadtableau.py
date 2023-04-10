import numpy as np
from tabulate import tabulate
with open('resultatstableaugpu.npy','rb') as f:
    lst = np.load(f,allow_pickle=True)

print(tabulate(lst, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))
