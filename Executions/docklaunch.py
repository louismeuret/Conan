import time
import os
import shutil
import subprocess
import numpy as np
import yaml
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
import logging
import psutil

# Configure the logging
logging.basicConfig(filename='docking.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
def docking_with_logging(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, ligand_info,shared_dict):
    # Log the start of docking
    logging.info(f"Starting docking for {ligand_info}")
    shared_dict[ligand_info] = 'Processing'

    # Perform the docking
    result = dck.docking(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, ligand_info)
    shared_dict[ligand_info] = 'Completed'

    # Log the completion of docking
    logging.info(f"Completed docking for {ligand_info}")

    # Log system performance
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    logging.info(f"CPU usage: {cpu_usage}%, RAM usage: {ram_usage}%")

    return result

def run_docking_process(threads, file_ligands, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results):
    # Create a multiprocessing pool
    p = mp.Pool(int(threads))

    # Run the docking process in parallel
    FAIL = list(
        tqdm(
            p.imap(
                functools.partial(
                    docking_with_logging,
                    software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results
                ),
                file_ligands
            ),
            total=len(file_ligands)
        )
    )

    # Close the multiprocessing pool
    p.close()
    p.join()

    return FAIL

async def monitor_docking_status(shared_dict):
    while True:
        # Clear the screen or print a new line for clarity
        print("\n" + "-" * 50)
        for ligand, status in shared_dict.items():
            print(f"Ligand {ligand}: {status}")
        await asyncio.sleep(5)  # Check every 5 seconds
        
def dockingtot(software2:str,nptsx:str,nptsy:str,nptsz:str,gridcenterx:str,gridcentery:str,gridcenterz:str,spacing:str,threads:str,nruns:str,pathdb:str,path_results:str,DEBUG_FLAG:bool):
    cwd = os.getcwd()
    cwd = cwd.replace("Executions", "")
    with open('../parameters/parameters_software/softwares.yaml', 'r') as file:
        softwares = yaml.safe_load(file)

    try:
        pathsoftware = shutil.which(softwares.get(software2, "")['exe_name'])
        if pathsoftware == None:
          raise Exception 
    except:
        pathsoftware = softwares.get(software2, "")['path']

    
    software_b = softwares.get(software2, "")['short_name']

    #listofpdbqt = glob.glob(pathdb)
    # Contient les paths complet de tout les ligands dans la db, recursivement
    listofpdbqt = glob.glob(f'{pathdb}/**/*.pdbqt', recursive=True) # /home/**/outputfile3186/outputfile3186.pdbqt
    print(f"Listofpdbqt: {listofpdbqt}")
    

    listofreceptors = glob.glob('../receptors/*.pdbqt')
    for receptor in listofreceptors:
        shutil.copy(receptor, f'{path_results}/RECEPTORS/')
    listofreceptors = glob.glob(f'{path_results}/RECEPTORS/*.pdbqt')
    print(listofreceptors)
    if software_b == "ad4" or software_b == "gpu": 
        dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors,path_results)
    else: 
        dirmaps = cv.create_dir(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors,path_results)

    startofdock = time.localtime(time.time())
    dossiertemps = f"{startofdock.tm_year}-{startofdock.tm_mon}-{startofdock.tm_mday}-{startofdock.tm_hour}:{startofdock.tm_min}"
    file_ligands = np.arange(1, len(listofpdbqt)+1, 1)
    print(file_ligands)
    """
    p = mp.Pool(int(threads))
    FAIL = list(
        tqdm(p.imap(
            functools.partial(
                dck.docking,software2,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,threads,nruns,pathdb,DEBUG_FLAG,listofpdbqt,dossiertemps,listofreceptors,dirmaps,cwd,pathsoftware,path_results
            ),
            [x for x in file_ligands],
        ),total=len(file_ligands))
    )
    p.close()
    return FAIL
    """
    """

    FAIL = []

    # Iterate over each file in file_ligands
    for file in tqdm(file_ligands, total=len(file_ligands)):
        # Call the docking function directly with all parameters for each file
        result = dck.docking(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, file, path_results)
        # Store the result
        FAIL.append(result)

    # Return the list of results
    return FAIL
    """


    
    run_docking_process(threads, file_ligands, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results)

    
    
    
    
    
