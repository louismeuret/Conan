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
import numpy as np


def parsepdbqt(pathpdbqt, software):
    cwd = os.getcwd()
    with open(pathpdbqt, "r+") as pdbqt:
        # read a list of lines into data
        pdbqtcontenu = pdbqt.readlines()

    highest = 0

    blockdata = ""
    if software == "VINA":
        findenergy = pdbqtcontenu[1].split()
        highest = float(findenergy[3])

    if software == "QVINA":
        findenergy = pdbqtcontenu[1].split()
        highest = float(findenergy[3])

    if software == "SMINA":
        findenergy = pdbqtcontenu[1].split()
        highest = float(findenergy[2])

    if software == "GPU":
        highest = 0

    if software == "GNINA":
        try:
            highest = [
                float(pdbqtcontenu[1].split()[2]),
                float(pdbqtcontenu[2].split()[2]),
                float(pdbqtcontenu[3].split()[2]),
            ]
        except:
            highest = [0,0,0]


    for x in range(len(pdbqtcontenu)):
        if pdbqtcontenu[x][:4] == "ATOM" or pdbqtcontenu[x][:6] == "HETATM":
            templine = pdbqtcontenu[x].split()
            pdbqtcontenu[x] = pdbqtcontenu[x][:-3]
            pdbqtcontenu[x] = pdbqtcontenu[x] + templine[2][:1] + "\n"
            blockdata = blockdata + pdbqtcontenu[x]
            # print(x)
        if software == "AD4":
            if pdbqtcontenu[x].startswith("USER    Estimated Free Energy of Binding"):
                highest = float(pdbqtcontenu[x].split("=")[1].split()[0])

        if pdbqtcontenu[x][:6] == "ENDMDL":
            break

            # print(x)
            # print(blockdata)
    return blockdata, highest


def compute_center_of_mass(mol, confId=-1):
    numatoms = mol.GetNumAtoms()
    conf = mol.GetConformer(confId)
    if not conf.Is3D():
        return 0
    # get cordinate of each atoms
    pts = np.array([list(conf.GetAtomPosition(atmidx)) for atmidx in range(numatoms)])
    atoms = [atom for atom in mol.GetAtoms()]
    mass = Descriptors.MolWt(mol)
    # get center of mass
    center_of_mass = (
        np.array(np.sum(atoms[i].GetMass() * pts[i] for i in range(numatoms))) / mass
    )
    # print(center_of_mass)
    return center_of_mass


def compute_descriptors(blockdata):
    try:
        m = Chem.rdmolfiles.MolFromPDBBlock(blockdata)
        complexitypdbqt = Chem.GraphDescriptors.BalabanJ(m)
        mollogppdbqt = Descriptors.MolLogP(m)
        molwtpdbqt = Descriptors.ExactMolWt(m)
        center_of_mass = compute_center_of_mass(m, -1)
    except:
        complexitypdbqt = 0
        mollogppdbqt = 0
        molwtpdbqt = 0
        center_of_mass = [0, 0, 0]

    return complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass


def findfiles(name, dir):
    newdir = pathlib.Path(dir)
    listfile = list(newdir.rglob("*" + name))
    liststr = [str(i) for i in listfile]
    return liststr


def processGPU(path):
    tofind = "best.pdbqt"
    tabresults = []
    listf = findfiles(tofind, path)
    for result in listf:
        free_energy = []
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "GPU")
        toparse = glob.glob("/".join(result.split("/")[:-1]) + "/*.xml")
        # print(toparse)
        toparse = toparse[0]
        tree = etree.parse(toparse)
        for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
            free_energy.append(float(user.text))
        highest = free_energy[0]
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest,
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )
    return tabresults


def processGNINA(path):
    tofind = "out.pdbqt"
    tabresults = []
    listf = findfiles(tofind, path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "GNINA")
        print(highest)
        pathbest = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest[0],
                highest[1],
                highest[2],
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )

    return tabresults


def processAD4(path):
    tofind = "log.txt"
    tabresults = []
    listf = findfiles(tofind, path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "AD4")
        pathbest = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest,
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )

    return tabresults


def processVINA(path):
    tofind = "out.pdbqt"
    tabresults = []

    listf = findfiles(tofind, path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "VINA")
        pathbest = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest,
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )

    return tabresults


def processSMINA(path):
    tofind = "out.pdbqt"
    tabresults = []

    listf = findfiles(tofind, path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "SMINA")
        pathbest = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest,
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )

    return tabresults


def processQVINA(path):
    tofind = "out.pdbqt"
    tabresults = []

    listf = findfiles(tofind, path)
    for result in listf:
        nomligand = result.split("/")[-2]
        blockdata, highest = parsepdbqt(result, "QVINA")
        pathbest = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        f = open(pathbest, "w")
        f.write(blockdata)
        f.close()
        complexitypdbqt, mollogppdbqt, molwtpdbqt, center_of_mass = compute_descriptors(
            blockdata
        )
        tabresults.append(
            [
                nomligand,
                highest,
                mollogppdbqt,
                molwtpdbqt,
                complexitypdbqt,
                center_of_mass,
            ]
        )

    return tabresults


def process_results(path, software):
    if software == "GPU":
        tabresults = processGPU(path)
    if software == "VINA":
        tabresults = processVINA(path)
    if software == "GNINA":
        tabresults = processGNINA(path)
    if software == "AD4":
        tabresults = processAD4(path)
    if software == "SMINA":
        tabresults = processSMINA(path)
    if software == "QVINA":
        tabresults = processQVINA(path)

    sortresultsnrj = sorted(tabresults, key=itemgetter(1), reverse=False)
    # print(tabulate(sortresults, headers = ["Nom ligand","Energy","CNNscore","CNNactivity","LogP","MolWt","Complexity"]))
    sortresultsabc = sorted(tabresults, key=itemgetter(0), reverse=False)
    # print(tabulate(sortresults, headers = ["Nom ligand","Energy","LogP","MolWt","Complexity"]))

    return sortresultsabc, sortresultsnrj


# process_results("/home/louis/Téléchargements/PROJETISDD/results_VINA","VINA")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GPU","GPU")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GNINA","GNINA")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_AD4","AD4")
