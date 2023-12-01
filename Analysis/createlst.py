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
    print(os.getcwd())
    newdir = "gninaresults/"+listefinale[x][0]
    try:
        os.umask(0)
        os.makedirs(newdir,mode=0o777)
    except:
        pass

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
    
    saveto = "gninaresults/"+listefinale[x][0]+"/"+listefinale[x][1]+".sdf.gz"
    sdffile = "gninaresults/"+listefinale[x][0]+"/"+listefinale[x][1]+".sdf"
    commandgnina = "./gnina -r "+receptor+" -l "+ligandtouse+" --minimize -o "+saveto
    os.system(commandgnina)

    with gzip.open(saveto, 'rb') as f_in:
        with open(sdffile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    with open(sdffile, "r+") as sdf:
        sdfcontenu = sdf.readlines()


    for r in range(len(sdfcontenu)):
        print(sdfcontenu[r])
        if sdfcontenu[r]==">  <minimizedAffinity>\n":

             resultsfinaux.append([listefinale[x][0],listefinale[x][1],float(sdfcontenu[r+1]),float(sdfcontenu[r+4]),float(sdfcontenu[r+7]),float(sdfcontenu[r+10])])
    #time.sleep(10)
    """
    subprocess.run(
    [
    "gnina",
    "-r",
    receptor,
    "-l",
    ligandtouse,
    "--minimize",
    "-o",
    saveto,
    ],
    stdout=open(os.devnull, "wb"),
    )
    """

#./gnina -r ConanVina/receptors/3wdc.pdb -l ConanGPU/testdock/results/DOCKED/outputfile1285/3wdc_Cyclomarin_align_clean_obabel_outputfile1285_outputfile1285/best.pdbqt --minimize -o minimized.sdf.gz
#listefinale = []
#listefinale = list(set(namevina+namegpu))
print(len(listefinale))
lst = sorted(resultsfinaux, key=itemgetter(4), reverse = True)
tempsorting = []
for x in range(200):
    tempsorting.append(lst[x])

resultsfinaux = tempsorting
print(resultsfinaux)
print(tabulate(resultsfinaux, headers = ["Nom ligand","Logiciel","Affinité minimisée","RMSD minimisé","CNNscore","CNNaffinity"]))
#for x in range(len(vina[]))
#ConanGPU/testdock/results/DOCKED/outputfile10/3wdc_Cyclomarin_align_clean_obabel_outputfile10_outputfile10/best.pdbqt
with open('resultatsgnina.npy','wb') as f:
    np.save(f,tempsorting)

#print(tabulate(lst, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))
