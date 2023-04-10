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
import createdirvina as cv
from tqdm import tqdm
import argparse
import gninadock as gd
import docking as dck

def dockingtot(software2:str,nptsx:str,nptsy:str,nptsz:str,gridcenterx:str,gridcentery:str,gridcenterz:str,spacing:str,threads:str,nruns:str,pathdb:str,DEBUG_FLAG:bool):
    cwd = os.getcwd()
    cwd = cwd.replace("Executions", "")
    try:
        pathsoftware = shutil.which(software2.lower())
        if pathsoftware == None:
          raise Exception 
    except:
        if software2 == "GPU":
            pathsoftware = cwd+"parametres/executables/autodock_gpu_128wi"
        elif software2 == "VINA":
            pathsoftware = cwd+"parametres/executables/vina"
        elif software2 == "GNINA":
            pathsoftware = cwd+"parametres/executables/gnina"
        elif software2 == "SMINA":
            pathsoftware = cwd+"parametres/executables/smina"
        elif software2 == "QVINA":
            pathsoftware = cwd+"parametres/executables/qvina"
        elif software2 == "AD4":
            pathsoftware = cwd+"parametres/executables/autodock4"
    #listofpdbqt = glob.glob(pathdb)
    # Contient les paths complet de tout les ligands dans la db, recursivement
    listofpdbqt = glob.glob(f'{pathdb}/**/*.pdbqt', recursive=True) # /home/**/outputfile3186/outputfile3186.pdbqt
    listofreceptors = glob.glob('../receptors/*.pdbqt')
    if software2 == "AD4" or software2 == "GPU": 
        dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors)
    else: 
        dirmaps = cv.create_dir(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors)

    startofdock = time.localtime(time.time())
    dossiertemps = f"{startofdock.tm_year}-{startofdock.tm_mon}-{startofdock.tm_mday}-{startofdock.tm_hour}:{startofdock.tm_min}"
    file_ligands = np.arange(1, len(listofpdbqt)+1, 1)
    print(file_ligands)
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
    
    
    
    
    
