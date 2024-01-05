import time
import os
import shutil
import subprocess
import numpy as np
#import createmaps as cm
import findpdbqt as find
import editligandpdbqt as edit
import dpfcreation as dpf
import fldcreation as fld
import centremasse as centre
import vinacreateconf as vcc
from multiprocessing import Pool
from multiprocessing import Process
import functools
import multiprocessing as mp
import glob
#import convertsdf as csdf
import os.path
import createmaps2 as cm
from tqdm import tqdm
import argparse
import gninadock as gd
import docking as dck

parser = argparse.ArgumentParser(description='Description de votre programme')

parser.add_argument('-software', type=str, help='Le nom du logiciel, AD4 pour Autodock4, GPU pour AutodockGPU, VINA pour Autodock Vina, et GNINA pour Gnina')
parser.add_argument('-nptsx', type=str, help='Le nombre de points dans la direction x')
parser.add_argument('-nptsy', type=str, help='Le nombre de points dans la direction y')
parser.add_argument('-nptsz', type=str, help='Le nombre de points dans la direction z')
parser.add_argument('-gridcenterx', type=str, help='La coordonnée x du centre de la grille')
parser.add_argument('-gridcentery', type=str, help='La coordonnée y du centre de la grille')
parser.add_argument('-gridcenterz', type=str, help='La coordonnée z du centre de la grille')
parser.add_argument('-spacing', type=str, help='L\'espacement entre les points de la grille')
parser.add_argument('-threads', type=str, help='Le nombre de threads à utiliser')
parser.add_argument('-nruns', type=str, help='Le nombre de runs de l\'agorithme génétique à effectuer')
parser.add_argument('-pathdb', type=str, help='Le chemin vers la base de données')
parser.add_argument('-DEBUG_FLAG', action='store_true', help='Activer le mode debug')

args = parser.parse_args()

# Accédez aux valeurs des arguments comme suit :
print(args.software)
print(args.nptsx)
print(args.nptsy)
print(args.nptsz)
print(args.gridcenterx)
print(args.gridcentery)
print(args.gridcenterz)
print(args.spacing)
print(args.threads)
print(args.nruns)
print(args.pathdb)
print(args.DEBUG_FLAG)

def dockingtot(software2:str,nptsx:str,nptsy:str,nptsz:str,gridcenterx:str,gridcentery:str,gridcenterz:str,spacing:str,threads:str,nruns:str,pathdb:str,DEBUG_FLAG:bool):
    cwd = os.getcwd()
    cwd = cwd.replace("Executions", "")
    try:
        pathsoftware = shutil.which(software2.lower())
        if pathsoftware == None:
          raise Exception 
    except:
        if software2 == "GPU":
            pathsoftware = cwd+"parameters/executables/autodock_gpu_128wi"
        elif software2 == "VINA":
            pathsoftware = cwd+"parameters/executables/vina"
        elif software2 == "GNINA":
            pathsoftware = cwd+"parameters/executables/gnina"
        elif software2 == "SMINA":
            pathsoftware = cwd+"parameters/executables/smina"
        elif software2 == "QVINA":
            pathsoftware = cwd+"parameters/executables/qvina"
        elif software2 == "AD4":
            pathsoftware = cwd+"parameters/executables/autodock4"
    #listofpdbqt = glob.glob(pathdb)
    # Contient les paths complet de tout les ligands dans la db, recursivement
    listofpdbqt = glob.glob(f'{pathdb}/**/*.pdbqt', recursive=True) # /home/**/outputfile3186/outputfile3186.pdbqt
    listofreceptors = glob.glob('../receptors/*.pdbqt')
    dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors)
    startofdock = time.localtime(time.time())
    dossiertemps = f"{startofdock.tm_year}-{startofdock.tm_mon}-{startofdock.tm_mday}-{startofdock.tm_hour}:{startofdock.tm_min}"
    file_ligands = np.arange(1, len(listofpdbqt), 1)
    p = mp.Pool(int(threads))
    FAIL = list(
        tqdm(p.imap(
            functools.partial(
                dck.docking,software2,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,threads,nruns,pathdb,DEBUG_FLAG,listofpdbqt,dossiertemps,listofreceptors,dirmaps,cwd,pathsoftware
            ),
            [x for x in file_ligands],
        ),total=len(file_ligands))
    )
    p.close()
    return FAIL
    
dockingtot(args.software,args.nptsx,args.nptsy,args.nptsz,args.gridcenterx,args.gridcentery,args.gridcenterz,args.spacing,args.threads,args.nruns,args.pathdb,False)  
    
    
    
