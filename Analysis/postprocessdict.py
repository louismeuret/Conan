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
root_dir = cwd + "results_GPU/DOCKED/"

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

#subfolders = [ f.path for f in os.scandir(cwd+"results/DOCKED/") if f.is_dir() ]

subfolders = fast_scandir(root_dir)

from os.path import exists
from lxml import etree
import centremasse as centre
meilleureenergie = 0
numberofsuccess = 0
numberofechec = 0
meilleurligand = ""

dictmaster = {}
tabcreation = []

print(len(subfolders))

for x in range(len(subfolders)):
        #print(x)
        #try:
        zincpdb = subfolders[x]+"/best.pdbqt"
        if os.path.exists(zincpdb) == True:
            
            str2=subfolders[x].split('/')
            n=len(str2)
            namezinc = str2[n-1]

            #print(namezinc)
            free_energy = []
            os.chdir(subfolders[x])
            toparse = glob.glob("*.xml")
            toparse = toparse[0]
            nameligand = toparse.strip(".xml") #toparse[:-10]
            #print(nameligand)
            #print(toparse)
            
            if nameligand not in dictmaster:
                #print(nameligand)
                #print("do not exist")
                dictmaster[nameligand] = {}


            dictmaster[nameligand][namezinc] = {}


            #tabcreation.append([])
            
            
            bestligandpaste = cwd+"results/BEST/" + namezinc + ".pdbqt"
            #shutil.copyfile(zincpdb, bestligandpaste)
            #print(toparse)
            
            with open(zincpdb, "r+") as pdbqt:
                # read a list of lines into data
                pdbqtcontenu = pdbqt.readlines()
                #print(pdbqtcontenu)

            blockdata = ""
            for x in range(len(pdbqtcontenu)):
                if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
                    templine = pdbqtcontenu[x].split()
                    pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
                    pdbqtcontenu[x] = pdbqtcontenu[x]+templine[2][:1]+"\n"
                    blockdata = blockdata + pdbqtcontenu[x]

            #print(blockdata)
            try:

                m = Chem.rdmolfiles.MolFromPDBBlock(blockdata)
                complexitypdb = Chem.GraphDescriptors.BalabanJ(m)
                mollogppdbqt = Descriptors.MolLogP(m)
                molwtpdbqt = Descriptors.ExactMolWt(m)
            except:
                pass

            
            tree = etree.parse(toparse)
            for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
                free_energy.append(float(user.text))
                # energy[test[count]] = float(user.text)
            highest = free_energy[0]
            #print(free_energy)
            #print(highest)
            if highest < meilleureenergie:
                meilleureenergie = highest
                meilleurligand = namezinc
            storenamezinc = namezinc




            centrex, centrey,centrez = centre.centremasse(blockdata)
            
            dictmaster[nameligand][namezinc]['energy'] = highest
            dictmaster[nameligand][namezinc]['nomligand'] = storenamezinc
            dictmaster[nameligand][namezinc]['coordx'] = centrex
            dictmaster[nameligand][namezinc]['coordy'] = centrey
            dictmaster[nameligand][namezinc]['coordz'] = centrez
            dictmaster[nameligand][namezinc]['logp'] = mollogppdbqt
            dictmaster[nameligand][namezinc]['molwt'] = molwtpdbqt
            dictmaster[nameligand][namezinc]['complexity'] = complexitypdb
            
            tabcreation.append([storenamezinc,highest,mollogppdbqt,molwtpdbqt,complexitypdb])

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

lst = sorted(tabcreation, key=itemgetter(1), reverse = False)
tempsorting = []
for x in range(33):
    tempsorting.append(lst[x])

goodfolder = cwd + "Analysis"
os.chdir(goodfolder)
#print(tabulate(tempsorting, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))
with open('resultatstableaugpu.npy','wb') as f:
    np.save(f,tempsorting)

with open('resultatstableaugpu.npy','rb') as f:
    lst = np.load(f)

print(tabulate(lst, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))













