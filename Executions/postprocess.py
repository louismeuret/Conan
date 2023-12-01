import os
import glob
import pathlib
cwd = os.getcwd()
from rdkit import Chem
from rdkit.Chem import GraphDescriptors
from rdkit.Chem import Descriptors
from tabulate import tabulate
from operator import itemgetter
from lxml import etree

def parsepdbqt(pathpdbqt,software):
    cwd = os.getcwd()
    with open(pathpdbqt, "r+") as pdbqt:
        # read a list of lines into data
        pdbqtcontenu = pdbqt.readlines()

    highest = 0

    blockdata = ""
    if software == "VINA":
        findenergy = pdbqtcontenu[1].split()
        highest = float(findenergy[3])

    if software == "GPU":
        highest = 0

    if software == "GNINA":
        try:
            findenergy = pdbqtcontenu[1].split("REMARK")
            highest = [float(findenergy[1].split()[1]),float(findenergy[2].split()[1]),float(findenergy[3].split()[1])]
        except:
            highest = [float(0),float(0),float(0)]


    for x in range(len(pdbqtcontenu)):
        if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
            templine = pdbqtcontenu[x].split()
            pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
            pdbqtcontenu[x] = pdbqtcontenu[x]+templine[2][:1]+"\n"
            blockdata = blockdata + pdbqtcontenu[x]
            #print(x)
        if software == "AD4":
            if pdbqtcontenu[x].startswith('USER    Estimated Free Energy of Binding'):
                highest = float(pdbqtcontenu[x].split('=')[1].split()[0])

        if pdbqtcontenu[x][:6] == "ENDMDL":
            break

                #print(x)
            #print(blockdata)
    return blockdata,highest

def compute_descriptors(blockdata):
    try:
        m = Chem.rdmolfiles.MolFromPDBBlock(blockdata)
        complexitypdbqt = Chem.GraphDescriptors.BalabanJ(m)
        mollogppdbqt = Descriptors.MolLogP(m)
        molwtpdbqt = Descriptors.ExactMolWt(m)
    except:
        complexitypdbqt = 0
        mollogppdbqt = 0
        molwtpdbqt = 0

    return complexitypdbqt,mollogppdbqt,molwtpdbqt


    

def findfiles(name,dir):
    newdir = pathlib.Path(dir)
    listfile = list(newdir.rglob("*"+name))
    liststr = [str(i) for i in listfile]
    return liststr


def processGPU(path):
    tofind = "best.pdbqt"
    tabresults = []
    listf = findfiles(tofind,path)
    for result in listf:

        free_energy = []
        nomligand = result.split('/')[-2]
        blockdata,highest = parsepdbqt(result,"GPU")
        toparse = glob.glob("/".join(result.split("/")[:-1])+"/*.xml")
        #print(toparse)
        toparse = toparse[0]
        tree = etree.parse(toparse)
        for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
            free_energy.append(float(user.text))
        highest = free_energy[0]
        complexitypdbqt,mollogppdbqt,molwtpdbqt = compute_descriptors(blockdata)
        tabresults.append([nomligand,highest,mollogppdbqt,molwtpdbqt,complexitypdbqt])
    return tabresults

def processGNINA(path):
    tofind = "out.pdbqt"
    tabresults = []
    listf = findfiles(tofind,path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result,"GNINA")
        pathbest = "/".join(result.split("/")[:-1])+"/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt,mollogppdbqt,molwtpdbqt = compute_descriptors(blockdata)
        tabresults.append([nomligand,highest[0],highest[1],highest[2],mollogppdbqt,molwtpdbqt,complexitypdbqt])

    return tabresults
       
def processAD4(path):
    tofind = "log.txt"
    tabresults = []
    listf = findfiles(tofind,path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result,"AD4")
        pathbest = "/".join(result.split("/")[:-1])+"/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt,mollogppdbqt,molwtpdbqt = compute_descriptors(blockdata)
        tabresults.append([nomligand,highest,mollogppdbqt,molwtpdbqt,complexitypdbqt])
    
    return tabresults

def processVINA(path):
    tofind = "out.pdbqt"
    tabresults = []

    listf = findfiles(tofind,path)
    for result in listf:
        nomligand = result.split('/')[-2]
        blockdata, highest = parsepdbqt(result,"VINA")
        pathbest = "/".join(result.split("/")[:-1])+"/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt,mollogppdbqt,molwtpdbqt = compute_descriptors(blockdata)
        tabresults.append([nomligand,highest,mollogppdbqt,molwtpdbqt,complexitypdbqt])
    
    return tabresults


def process_results(path,software):
    if software == "GPU":
        tabresults = processGPU(path)
    if software == "VINA":
        tabresults = processVINA(path)
    if software == "GNINA":
        tabresults = processGNINA(path)
    if software == "AD4":
        tabresults = processAD4(path)

    sortresultsnrj = sorted(tabresults, key=itemgetter(1), reverse = False)
    #print(tabulate(sortresults, headers = ["Nom ligand","Energy","CNNscore","CNNactivity","LogP","MolWt","Complexity"]))
    sortresultsabc = sorted(tabresults, key=itemgetter(0), reverse = False)
    #print(tabulate(sortresults, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))

    return sortresultsabc,sortresultsnrj


#process_results("/home/louis/Téléchargements/PROJETISDD/results_VINA","VINA")
#process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GPU","GPU")
#process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GNINA","GNINA")
#process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_AD4","AD4")

