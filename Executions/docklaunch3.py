import time
import os
import shutil
import numpy as np
import yaml
import glob
import asyncio
import concurrent.futures
from multiprocessing import Manager
import argparse

import threading
import logging
import createmaps2 as cm
import createdirvina as cv
import docking as dck

# Configure the logging


def create_subfolders(results_folder):
    try:
        subfolders = ["DOCKED", "PARAMETERS", "FILES", "RESULTS","MAPS","RECEPTORS"]
        for subfolder in subfolders:
            path = os.path.join(results_folder, subfolder)
            os.makedirs(path, exist_ok=True)
            logging.info(f"{path} created")
    except Exception as e:
        logging.error(f"An error occurred while creating subfolders: {e}")
    

def docking_with_logging(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, status_dict, ligand_info):
    logging.basicConfig(filename=f'{path_results}/FILES/docking_launch.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', force=True)
    logging.info(f"Starting docking for {ligand_info}")

    status_dict[ligand_info] = 'Processing'
    # Perform the docking
    
    result = dck.docking(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, ligand_info)
    
    status_dict[ligand_info] = 'Completed'

    logging.info(f"Completed docking for {ligand_info}")
    return result

async def monitor_docking_status(status_dict):
    while True:
        logging.info(str(dict(status_dict)))  # Convert manager dict to regular dict for logging
        await asyncio.sleep(5)  # Check status every 5 seconds


def start_async_monitoring(status_file):
    asyncio.run(monitor_docking_status(status_file))

def dockingtot(software2, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG,path_results=None,status_dict=None):
    cwd = os.getcwd()
    cwd = cwd.replace("Executions", "")
    if path_results is None: 
        path_results = os.path.join(f"results_{software2}")
    create_subfolders(path_results)

    with open('../parameters/parameters_software/softwares.yaml', 'r') as file:
        softwares = yaml.safe_load(file)

    try:
        pathsoftware = shutil.which(softwares.get(software2, "")['exe_name'])
        if pathsoftware is None:
            logging.info(f"{software2} not in path, using file in executable folder")
            raise Exception  
        else:
            logging.info(f"using {software2} in PATH")

    except:
        pathsoftware = softwares.get(software2, "")['path']

    software_b = softwares.get(software2, "")['short_name']
    listofpdbqt = glob.glob(f'{pathdb}/**/*.pdbqt', recursive=True)
    listofreceptors = glob.glob('../receptors/*.pdbqt')
    for receptor in listofreceptors:
        shutil.copy(receptor, f'{path_results}/RECEPTORS/')
    listofreceptors = glob.glob(f'{path_results}/RECEPTORS/*.pdbqt')
    logging.info(f"List of receptors found: {listofreceptors}")
    
    if software_b in ["ad4", "gpu"]: 
        dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors, path_results)
        logging.info(f"Maps Created: {dirmaps}")
    else: 
        dirmaps = cv.create_dir(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors, path_results)
        logging.info(f"Dirs Created: {dirmaps}")

    startofdock = time.localtime(time.time())
    dossiertemps = f"{startofdock.tm_year}-{startofdock.tm_mon}-{startofdock.tm_mday}-{startofdock.tm_hour}:{startofdock.tm_min}"
    file_ligands = np.arange(1, len(listofpdbqt)+1, 1)
    #file_ligands = listofpdbqt
    if status_dict is None:
        with Manager() as manager:
            status_dict = manager.dict()

            status_dict.update({ligand_info: 'Pending' for ligand_info in file_ligands})
                
            monitoring_thread = threading.Thread(target=start_async_monitoring, args=(status_dict,))
            monitoring_thread.start()

            with concurrent.futures.ProcessPoolExecutor(max_workers=int(threads)) as executor:

                futures = {executor.submit(docking_with_logging, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, status_dict, ligand): ligand for ligand in file_ligands}
                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    ligand_info = futures[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        logging.error(f"{ligand_info} generated an exception: {exc}")
                        status_dict.update({ligand_info: f"ERROR: {exc}"})
            monitoring_thread.join()
    else:
        monitoring_thread = threading.Thread(target=start_async_monitoring, args=(status_dict,))
        monitoring_thread.start()

        with concurrent.futures.ProcessPoolExecutor(max_workers=int(threads)) as executor:

            futures = {executor.submit(docking_with_logging, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, status_dict, ligand): ligand for ligand in file_ligands}
            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                ligand_info = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    logging.error(f"{ligand_info} generated an exception: {exc}")
        monitoring_thread.join()
    



if __name__ == '__main__':
    #dockingtot("Autodock4", "50", "76", "74", "11.356", "0", "8.729", "1", "6", "100", "/home/cya/Conan/db_ligands", True,"/home/cya/Conan/results_test")

    parser = argparse.ArgumentParser(description='Run docking simulations with Conan.')
    
    parser.add_argument('--software', help='Docking software to use', required=True)
    parser.add_argument('--nptsx', help='Number of points in x direction', type=int, required=True)
    parser.add_argument('--nptsy', help='Number of points in y direction', type=int, required=True)
    parser.add_argument('--nptsz', help='Number of points in z direction', type=int, required=True)
    parser.add_argument('--gridcenterx', help='Grid center x coordinate', type=float, required=True)
    parser.add_argument('--gridcentery', help='Grid center y coordinate', type=float, required=True)
    parser.add_argument('--gridcenterz', help='Grid center z coordinate', type=float, required=True)
    parser.add_argument('--spacing', help='Grid spacing', type=float, required=True)
    parser.add_argument('--threads', help='Number of threads to use', type=int, required=True)
    parser.add_argument('--nruns', help='Number of runs', type=int, required=True)
    parser.add_argument('--pathdb', help='Path to the database of ligands', required=True)
    parser.add_argument('--debug', help='Enable debug mode (display more info about what is being done by the software)', type=bool, required=False, default=False)
    parser.add_argument('--path_results', help='Path to save results', default=None, required=False)
    #parser.add_argument('--status_dict', help='Status dictionary', default=None, required=False)

    args = parser.parse_args()

    dockingtot(args.software, args.nptsx, args.nptsy, args.nptsz, 
               args.gridcenterx, args.gridcentery, args.gridcenterz, 
               args.spacing, args.threads, args.nruns, args.pathdb, 
               args.debug, args.path_results, args.status_dict)

