import time
import os
import shutil
import subprocess
import numpy as np
import yaml
import asyncio
import threading
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
def docking_with_logging(queue, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, ligand_info):
    # Log the start of docking
    logging.info(f"Starting docking for {ligand_info}")

    # Validate that queue is a Manager().Queue()
    if not isinstance(queue, mp.queues.Queue):
        logging.error("Invalid queue object passed to docking_with_logging")
        print(type(queue))
        return

    queue.put((ligand_info, 'Processing'))

    # Perform the docking
    result = dck.docking(software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, ligand_info)
    queue.put((ligand_info, 'Completed'))

    # Log the completion of docking
    logging.info(f"Completed docking for {ligand_info}")
    return result

def run_docking_process(threads, file_ligands, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, queue):
    with mp.Pool(int(threads)) as pool:
        func = functools.partial(docking_with_logging, queue, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results)
        results = list(tqdm(pool.imap(func, file_ligands), total=len(file_ligands)))
    return results

async def monitor_docking_status(queue):
    status_dict = {}
    while True:
        while not queue.empty():
            ligand_info, status = queue.get()
            status_dict[ligand_info] = status

        print("\n" + "-" * 50)
        for ligand, status in status_dict.items():
            print(f"Ligand {ligand}: {status}")

        await asyncio.sleep(5)

def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

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
    queue = mp.Queue()
    docking_process = mp.Process(target=run_docking_process, args=(queue, file_ligands, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, threads, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results))
    docking_process.start()

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_async_loop, args=(loop,))
    t.start()

    asyncio.run_coroutine_threadsafe(monitor_docking_status(queue), loop)

    docking_process.join()
    loop.call_soon_threadsafe(loop.stop)
    t.join()

    docking_process.join() 
    """
    manager = mp.Manager()
    queue = manager.Queue()

    docking_process = mp.Process(target=run_docking_process, args=(threads, file_ligands, software_b, nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, nruns, pathdb, DEBUG_FLAG, listofpdbqt, dossiertemps, listofreceptors, dirmaps, cwd, pathsoftware, path_results, queue))
    docking_process.start()

    # Start the monitoring
    asyncio.run(monitor_docking_status(queue))

    docking_process.join()

if __name__ == '__main__':
    # Execute the docking process in main mode
    # Used as test
    dockingtot("Autodock-vina", 50, 76, 74, 11.356, 0, 8.729, 1, 6, 100, "/home/cya/Conan/db_ligands", "/home/cya/Conan/results_test", True)
