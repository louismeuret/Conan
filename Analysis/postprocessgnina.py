import os
import shutil
import glob

cwd = os.getcwd()
from rdkit import Chem
from rdkit.Chem import GraphDescriptors
from rdkit.Chem import Descriptors
import json
import scipy.io as sio
#from rdkit import GraphDescriptors
from tabulate import tabulate
from operator import itemgetter
import numpy as np

cwd = cwd.replace("Analysis","")
root_dir = cwd + "results_GNINA/DOCKED/"
print(root_dir)
def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

#subfolders = [ f.path for f in os.scandir(cwd+"results_VINA/DOCKED/") if f.is_dir() ]

subfolders = fast_scandir(root_dir)
print(subfolders)
from os.path import exists
from lxml import etree
import centremasse as centre
import time
meilleureenergie = 0
numberofsuccess = 0
numberofechec = 0
meilleurligand = ""

dictmaster = {}
tabcreation = []
def extract_energy_and_atoms(filename):
    atoms = []

    with open(filename, 'r') as f:
        for line in f:
            print(line)
            if line.startswith('ATOM'):
                atoms.append(line)
            elif line.startswith('ENDMDL'):
                break
print(len(subfolders))
for x in range(len(subfolders)):
        #print(x)
        #try:
        zincpdb = subfolders[x]+"/out.pdbqt"
        if os.path.exists(zincpdb) == True:
            
            str2=subfolders[x].split('/')
            n=len(str2)
            namezinc = str2[n-1]

            #print(namezinc)
            free_energy = []
            os.chdir(subfolders[x])
            #print(nameligand)
            #print(toparse)
            toparse = glob.glob("*.pdbqt")
            toparse = toparse[0]
            nameligand = toparse.strip(".pdbqt") #toparse[:-10]
            
            if nameligand not in dictmaster:
                #print(nameligand)
                #print("do not exist")
                dictmaster[nameligand] = {}
                

            dictmaster[nameligand][namezinc] = {}
    
            #tabcreation.append([])
            
            #getting the results of energy
            """
            results_file=open('%s/log.txt'%(subfolders[x]),'r')
            for i in results_file.readlines():
                resenergy=i.split()
                try:
                    if int(resenergy[0])==1:
                        #print(j,x[0],x[1])
                        highest = float(resenergy[1])
                        print(highest)
                except:
                    pass
            """
            with open(zincpdb, "r+") as pdbqt:
                # read a list of lines into data
                pdbqtcontenu = pdbqt.readlines()
                #print(pdbqtcontenu)
            
            try: 
                blockdata = ""
                findenergy = pdbqtcontenu[1].split("REMARK")
                #findenergy = ['', ' minimizedAffinity -6.45454311', ' CNNscore 0.567627668', ' CNNaffinity 5.05423784', '  8 active torsions:\n']
                highest = float(findenergy[1].split()[1])
                CNNscore = float(findenergy[2].split()[1])
                CNNaffinity = float(findenergy[3].split()[1])
            except:
                print(zincpdb)

            print(highest)

            for x in range(len(pdbqtcontenu)):
                if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
                    templine = pdbqtcontenu[x].split()
                    pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
                    pdbqtcontenu[x] = pdbqtcontenu[x]+templine[2][:1]+"\n"
                    blockdata = blockdata + pdbqtcontenu[x]
                    #print(x)
                if pdbqtcontenu[x][:6] == "ENDMDL":
                    print("break")
                    break
                #print(x)
            f = open(namezinc+"best.pdbqt", "w")
            f.write(blockdata)
            f.close()
            #print(blockdata)
            try:

                m = Chem.rdmolfiles.MolFromPDBBlock(blockdata)
                complexitypdb = Chem.GraphDescriptors.BalabanJ(m)
                mollogppdbqt = Descriptors.MolLogP(m)
                molwtpdbqt = Descriptors.ExactMolWt(m)
            except:
                pass

            
            #print(free_energy)
            #print(highest)
            if highest < meilleureenergie:
                meilleureenergie = highest
                meilleurligand = namezinc
            storenamezinc = namezinc


            #centrex = 10
            #centrey = 15
            #centrez = 22
            
            #print(blockdata)
            centrex, centrey,centrez = centre.centremasse(blockdata)
            
            dictmaster[nameligand][namezinc]['energy'] = highest
            dictmaster[nameligand][namezinc]['nomligand'] = storenamezinc
            dictmaster[nameligand][namezinc]['coordx'] = centrex
            dictmaster[nameligand][namezinc]['coordy'] = centrey
            dictmaster[nameligand][namezinc]['coordz'] = centrez
            dictmaster[nameligand][namezinc]['logp'] = mollogppdbqt
            dictmaster[nameligand][namezinc]['molwt'] = molwtpdbqt
            dictmaster[nameligand][namezinc]['complexity'] = complexitypdb
            
            tabcreation.append([storenamezinc,highest,CNNscore,CNNaffinity,mollogppdbqt,molwtpdbqt,complexitypdb])

            numberofsuccess = numberofsuccess + 1

        else:
            
            numberofechec = numberofechec + 1

print(tabcreation)
print("meilleur energie:")
print(meilleureenergie)
print("de: ")
print(meilleurligand)
print("succès: ")
print(numberofsuccess)
print("echcecs: ")
print(numberofechec)
#etree.tostring(root, pretty_print=True)

#print(dictmaster)
dictjson = json.dumps(dictmaster)
#print(dictjson)
pathdict = "resultsAUTODOCKclp.json"

test = open(pathdict, 'w+')
try:
    json.dump(dictmaster, test)
finally:
    test.close()

#print(tabulate(tabcreation, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))

lst = sorted(tabcreation, key=itemgetter(0), reverse = False)
tempsorting = []
for x in range(33):
    tempsorting.append(lst[x])

goodfolder = cwd + "Analysis"
os.chdir(goodfolder)
#print(tabulate(tempsorting, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))
with open('resultatstableauvina.npy','wb') as f:
    np.save(f,tempsorting)

with open('resultatstableauvina.npy','rb') as f:
    lst = np.load(f)

print(tabulate(lst, headers = ["Nom ligand","Energy","CNNscore","CNNactivity","LogP","MolWt","Complexity"]))












