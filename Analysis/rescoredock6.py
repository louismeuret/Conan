import numpy as np
import subprocess
from tabulate import tabulate
import time
import os
import gzip
import shutil
from operator import itemgetter

with open('resultatstableau.npy','rb') as f:
    vina = np.load(f,allow_pickle=True)

with open('resultatstableaugpu.npy','rb') as f:
    gpu = np.load(f,allow_pickle=True)

print(len(vina))
namevina = []
namegpu = []
listefinale = []

os.chdir("../../")
cwd = os.getcwd()
for x in range(len(vina)):
    listefinale.append([vina[x][0],"VINA"])
    listefinale.append([gpu[x][0],"GPU"])

print(listefinale)
resultsfinaux = []
for x in range(len(listefinale)):
    print(x)
    print(listefinale[x][0])
    data = listefinale[x][0].split("_")
    receptor = "ConanVina/receptors/"+data[0]+".pdb"
    print(data)

    if listefinale[x][1] == "VINA":
        pathligand = "ConanVina/results_VINA/DOCKED/"+data[5]+"/"+listefinale[x][0]+"/"+"out.pdbqt"
        pathsave = "ConanVina/results_VINA/DOCKED/"+data[5]+"/"+listefinale[x][0]+"/"+"save.pdbqt"

        with open(pathligand, "r+") as pdbqt:
                # read a list of lines into data
            pdbqtcontenu = pdbqt.readlines()
                #print(pdbqtcontenu)
            
            
        blockdata = ""
        for z in range(1,len(pdbqtcontenu)):
            if pdbqtcontenu[z][:6] == "ENDMDL":
                print("break")
                break
            blockdata = blockdata + pdbqtcontenu[z]
        
        with open(pathsave,'w+') as f:
            f.write(blockdata)
        ligandtouse = pathsave

    if listefinale[x][1] == "GPU":
        ligandtouse = "testdock/results/DOCKED/"+data[5]+"/"+listefinale[x][0]+"/"+"best.pdbqt"
    
    pathdock6 = "resultsdock6/"+data[5]+"/"+listefinale[x][0]+"/"+listefinale[x][1]+"/"
    pathmol2 = pathdock6 + data[5]+".mol2"
    os.makedirs(pathdock6)
    commandobabel = "obabel -ipdbqt %s -omol2 -O %s"%(ligandtouse,pathmol2)
    print(commandobabel)
    os.system(commandobabel)
    os.chdir(pathdock6)
    commandprepareamber = "perl /media/gauto/ec3a8e80-b5f3-42fd-a620-de628a10967a/diego/softwares/DOCK6_SOFTWARE/dock6/bin/prepare_amber.pl %s %s"%(pathmol2,receptor)
    print(commandprepareamber)
    os.system(commandprepareamber)
    os.chdir(cwd)

    with open("Analysis/dock.in", "r+") as dockin:
        incontenu = dockin.readlines()

    contenudockin = ""
    for r in range(len(incontenu)):
        if r == 2:
            incontenu[r] = "ligand_atom_file                                             "+data[5]+".mol2\n"
        if r == 35:
            incontenu[r] = "amber_score_receptor_file_prefix                             "+data[0]+"\n"
        contenudockin = contenudockin + incontenu[r]
    pathsavedockin = pathdock6+"dock.in"
    with open(pathsavedockin,'w+') as f:
        f.write(contenudockin)

    os.chdir(pathdock6)
    commanddock6 = "/media/gauto/ec3a8e80-b5f3-42fd-a620-de628a10967a/diego/softwares/DOCK6_SOFTWARE/dock6/bin/dock6 -i dock.in -o dock.out"
    print(commanddock6)
    os.system(commanddock6)


