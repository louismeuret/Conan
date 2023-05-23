from pymol import cmd
from pymol import cgo

import pymol
import sys
import pickle


#cmd.set("cgo_transparency", 0.5)

# Accédez aux valeurs des arguments comme suit :
print(sys.argv[1])
ligandlist = pickle.load(open(sys.argv[1], "rb"))
print("IN LAUNCH PYMOL")
print(ligandlist)

energy_values = list()
for sublist in ligandlist:
    energy_values.append(sublist[-1])

norm = matplotlib.colors.Normalize(vmin=min(energy_values), vmax=max(energy_values))
print(norm)
colors = plt.cm.seismic(norm(energy_values))
pymol.finish_launching()
for ligand in range(len(ligandlist)):
    name = ligandlist[ligand][0]
    coordx = ligandlist[ligand][1]
    coordy = ligandlist[ligand][2]
    coordz = ligandlist[ligand][3]
    r = colors[ligand][0]
    g = colors[ligand][1]
    b = colors[ligand][2]

    newligand = [cgo.COLOR, r, g, b, cgo.SPHERE, coorx, coordy, coordz, 0.5]
    cmd.load_cgo(newligand, name)

#cmd.load(str(sys.argv[2]))

