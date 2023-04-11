import createmaps2 as cm
import glob
import os

nptsx = "90"
nptsy = "75"
nptsz = "85"

gridcenterx = "55"
gridcentery = "-21"
gridcenterz = "-20"

numberofruns = "100"
spacing = "0.375" 

cwd = os.getcwd()
cwd = cwd.replace("Executions", "")

list_of_receptors = glob.glob('../receptors/*.pdbqt') 

dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, list_of_receptors)
print(dirmaps)
