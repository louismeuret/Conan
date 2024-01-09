import time
import os
import subprocess
import editligandpdbqt as edit
import dpfcreation as dpf
import fldcreation as fld
import fldcreationAD4 as fld2
import vinacreateconf as vcc
from multiprocessing import Process
import argparse
import logging


def docking(
    software: str,
    nptsx: str,
    nptsy: str,
    nptsz: str,
    gridcenterx: str,
    gridcentery: str,
    gridcenterz: str,
    spacing: str,
    threads: str,
    nruns: str,
    pathdb: str,
    DEBUG_FLAG: bool,
    listofpdbqt: list,
    dossiertemps: str,
    listofreceptors: list,
    dirmaps: list,
    cwd: str,
    pathsoftware: str,
    path_results: str,
    ligandnumber,
):
    logging.basicConfig(filename='docking.log', level=logging.INFO, format='%(asctime)s:%(levelname)s: %(message)s')

    def run_command(command, debug_flag):
        print(command)
        if debug_flag:
            subprocess.run(command)
        else:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    try:
        #DEBUG_FLAG = True
        currentligand = listofpdbqt[ligandnumber - 1]
        print(listofpdbqt)
        print("listofreceptors:")
        print(listofreceptors)
        #ligandfilename = currentligand.split("/")[-1]  # outputfile34.pdbqt
        ligandfilename = os.path.basename(currentligand)

        ligandfirstpath = os.path.splitext(os.path.basename(currentligand))[0]
        # ligandfirstpath = "outputfile"+str(ligandnumber)

        # print(ligandfirstpath)
        liganddocktime1 = time.time()

        # Execution du docking sur chacun des recepteurs
        for receptor in range(len(listofreceptors)):
            receptor_basename = os.path.basename(listofreceptors[receptor])
            receptor_name = receptor_basename[:-6]
            #receptor_dir = os.path.dirname(listofreceptors[receptor])
            receptor_path = listofreceptors[receptor]
            map_dir = dirmaps[receptor]

            os.chdir(cwd)

            # Check and create configuration file for docking software
            if software in ["vina", "smina", "qvina-w", "qvina2.1"]:
                config_file_path = os.path.join(map_dir, receptor_name + ".txt")
                if not os.path.isfile(config_file_path):
                    vcc.createconf(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, receptor_path, receptor_name, path_results)

            ligand_path, ligand_full_path, ligand_name = edit.editligandpdbqt(software, currentligand, receptor_name, dossiertemps, ligandfilename, cwd, ligandfirstpath, path_results)
            dpf_location = os.path.join(ligand_path, "DOCKING.dpf")

            if DEBUG_FLAG:
                debug_info = (
                    f"Software: {software}\n"
                    f"Ligand file total: {currentligand}\n"
                    f"Path ligand: {ligand_full_path}\n"
                    f"Receptor: {receptor_name}\n"
                    f"Path db: {pathdb}\n"
                    f"Dir maps: {map_dir}\n"
                )
                print(debug_info)
            print("HERE")   
            """     
            if software in ["gpu", "ad4"]:
                ligand_type = dpf.dpfcreation(ligand_full_path, receptor_path, dpf_location, map_dir, cwd, receptor_name, software)
                if software == "gpu":
                    fld.fldcreation(ligand_type, map_dir, ligand_path, gridcenterx, gridcentery, gridcenterz, cwd, receptor_name, nptsx, nptsy, nptsz, spacing, path_results)
                elif software == "ad4":
                    fld2.fldcreation(ligand_type, map_dir, ligand_path, gridcenterx, gridcentery, gridcenterz, cwd, receptor_name, nptsx, nptsy, nptsz, spacing, path_results)
            """
            pathout = ligand_path + "out.pdbqt"
            print(f"PATHOUT = {pathout}")
            print(os.path.isfile(pathout))
            if not os.path.isfile(pathout):
                command = [
                    pathsoftware,
                    "--config", config_file_path,
                    "--ligand", ligand_full_path,
                    "--out", f"{pathout}",
                    "--log", f"{ligand_path}log.txt"
                ]
                print(command)

                if software in ["vina", "smina", "qvina-w", "qvina2.1"]:
                    run_command(command, DEBUG_FLAG)

                if software in ["gpu", "ad4"]:
                    numberofruns = nruns
                    command = [
                        pathsoftware,
                    ]
                    additional_params = ["--import_dpf", dpflocation, "--nrun", numberofruns, "--gbest", "1"]
                    if software == "ad4":
                        additional_params = ["-p", dpflocation, "-l", f"{pathligand}log.txt"]
                    command.extend(additional_params)
                    run_command(command, DEBUG_FLAG)

                if software == "gnina":
                    command = [
                        pathsoftware,
                        "-r", receptor_path,
                        "-l", ligand_full_path,
                        "-o", f"{ligand_path}out.pdbqt",
                        "--center_x", gridcenterx,
                        "--center_y", gridcentery,
                        "--center_z", gridcenterz,
                        "--size_x", nptsx,
                        "--size_y", nptsy,
                        "--size_z", nptsz,
                        "--log", f"{ligand_path}out.log"
                    ]
                    run_command(command, DEBUG_FLAG)

        liganddocktime2 = time.time()
        liganddocktimetotal = liganddocktime2 - liganddocktime1
        print(
            "temps de dock %s secondes, ligand: %s"
            % (liganddocktimetotal, ligandfirstpath),
            end="",
        )
        logging.info(f"Docking time for {ligandfirstpath}: {liganddocktimetotal} seconds")
        Failed = ligandnumber

    except Exception as e:
        logging.error(f"Error occurred during docking of ligand {ligandnumber}: {e}")
        return None

    return Failed
