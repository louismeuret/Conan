import os
import glob
import pathlib
from rdkit import Chem
from rdkit.Chem import GraphDescriptors
from rdkit.Chem import Descriptors
from tabulate import tabulate
from operator import itemgetter
from lxml import etree
import numpy as np
from tqdm import tqdm


def parse_pdbqt(path_pdbqt, software):
    with open(path_pdbqt, "r+") as pdbqt:
        pdbqt_content = pdbqt.readlines()

    highest = 0

    if software in ["VINA", "QVINA", "SMINA"]:
        find_energy = pdbqt_content[1].split()
        if software in ["VINA", "QVINA"]:
            highest = float(find_energy[3])
        elif software == "SMINA":
            highest = float(find_energy[2])

    if software == "GNINA":
        try:
            highest = [float(pdbqt_content[1].split()[2]), float(pdbqt_content[2].split()[2]), float(pdbqt_content[3].split()[2])]
        except:
            highest = [0, 0, 0]

    for x in range(len(pdbqt_content)):
        if pdbqt_content[x][:4] == "ATOM" or pdbqt_content[x][:6] == "HETATM":
            temp_line = pdbqt_content[x].split()
            pdbqt_content[x] = pdbqt_content[x][:-3] + temp_line[2][:1] + "\n"
        if "ENDMDL" in pdbqt_content:
            break

    if software == "AD4":
        for line in pdbqt_content:
            if line.startswith("USER    Estimated Free Energy of Binding"):
                highest = float(line.split("=")[1].split()[0])
            if "ENDMDL" in pdbqt_content:
                break

    return "".join(pdbqt_content), highest


def compute_center_of_mass(mol, conf_id=-1):
    num_atoms = mol.GetNumAtoms()
    conf = mol.GetConformer(conf_id)
    if not conf.Is3D():
        return 0
    pts = np.array([list(conf.GetAtomPosition(atm_idx)) for atm_idx in range(num_atoms)])
    atoms = [atom for atom in mol.GetAtoms()]
    mass = Descriptors.MolWt(mol)
    center_of_mass = np.array(np.sum(atoms[i].GetMass() * pts[i] for i in range(num_atoms))) / mass
    return center_of_mass


def compute_descriptors(block_data):
    try:
        m = Chem.rdmolfiles.MolFromPDBBlock(block_data)
        complexity_pdbqt = Chem.GraphDescriptors.BalabanJ(m)
        mol_logp_pdbqt = Descriptors.MolLogP(m)
        mol_wt_pdbqt = Descriptors.ExactMolWt(m)
        center_of_mass = compute_center_of_mass(m, -1)
    except:
        complexity_pdbqt = 0
        mol_logp_pdbqt = 0
        mol_wt_pdbqt = 0
        center_of_mass = [0, 0, 0]

    return complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass


def find_files(name, dir):
    new_dir = pathlib.Path(dir)
    list_file = list(new_dir.rglob("*" + name))
    list_str = [str(i) for i in list_file]
    return list_str


def process_GPU(path):
    to_find = "best.pdbqt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing GPU results'):
        free_energy = []
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "GPU")
        to_parse = glob.glob("/".join(result.split("/")[:-1]) + "/*.xml")[0]
        tree = etree.parse(to_parse)
        for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
            free_energy.append(float(user.text))
        highest = free_energy[0]
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest, mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_GNINA(path):
    to_find = "out.pdbqt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing GNINA results'):
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "GNINA")
        path_best = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        with open(path_best, "w") as f:
            f.write(block_data)
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest[0], highest[1], highest[2], mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_AD4(path):
    to_find = "log.txt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing AD4 results'):
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "AD4")
        path_best = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        with open(path_best, "w") as f:
            f.write(block_data)
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest, mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_VINA(path):
    to_find = "out.pdbqt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing VINA results'):
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "VINA")
        path_best = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        with open(path_best, "w") as f:
            f.write(block_data)
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest, mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_SMINA(path):
    to_find = "out.pdbqt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing SMINA results'):
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "SMINA")
        path_best = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        with open(path_best, "w") as f:
            f.write(block_data)
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest, mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_QVINA(path):
    to_find = "out.pdbqt"
    tab_results = []
    list_f = find_files(to_find, path)
    for result in tqdm(list_f, desc='Processing QVINA results'):
        nom_ligand = result.split("/")[-2]
        block_data, highest = parse_pdbqt(result, "QVINA")
        path_best = "/".join(result.split("/")[:-1]) + "/best.pdbqt"
        with open(path_best, "w") as f:
            f.write(block_data)
        complexity_pdbqt, mol_logp_pdbqt, mol_wt_pdbqt, center_of_mass = compute_descriptors(block_data)
        tab_results.append([nom_ligand, highest, mol_logp_pdbqt, mol_wt_pdbqt, complexity_pdbqt, center_of_mass])
    return tab_results


def process_results(path, software):
    if software == "GPU":
        tab_results = process_GPU(path)
    elif software == "VINA":
        tab_results = process_VINA(path)
    elif software == "GNINA":
        tab_results = process_GNINA(path)
    elif software == "AD4":
        tab_results = process_AD4(path)
    elif software == "SMINA":
        tab_results = process_SMINA(path)
    elif software == "QVINA":
        tab_results = process_QVINA(path)

    sort_results_nrj = sorted(tab_results, key=itemgetter(1), reverse=False)
    sort_results_abc = sorted(tab_results, key=itemgetter(0), reverse=False)

    return sort_results_abc, sort_results_nrj


# process_results("/home/louis/Téléchargements/PROJETISDD/results_VINA","VINA")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GPU","GPU")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_GNINA","GNINA")
# process_results("/home/louis/Téléchargements/PROJETISDD/BLINDDOCK/results_AD4","AD4")
