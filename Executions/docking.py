import time
import os
import shutil
import subprocess
import numpy as np

# import createmaps as cm
import findpdbqt as find
import editligandpdbqt as edit
import dpfcreation as dpf
import fldcreation as fld
import fldcreationAD4 as fld2
import centremasse as centre
import vinacreateconf as vcc
from multiprocessing import Pool
from multiprocessing import Process
import multiprocessing as mp
import glob
import convertsdf as csdf
import os.path
import createmaps2 as cm
from tqdm import tqdm
import argparse
import gninadock as gd


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
    ligandnumber,
):
    # print(FAIL)

    # Full path
    # print(DEBUG_FLAG)
    DEBUG_FLAG = True
    currentligand = listofpdbqt[ligandnumber - 1]
    print(listofpdbqt)
    ligandfilename = currentligand.split("/")[-1]  # outputfile34.pdbqt

    ligandfirstpath = currentligand.split("/")[-1][:-6]  # outputfile34
    # ligandfirstpath = "outputfile"+str(ligandnumber)

    # print(ligandfirstpath)
    liganddocktime1 = time.time()

    # Execution du docking sur chacun des recepteurs
    for receptor in range(len(listofreceptors)):
        # try:
        # Failed = False
        # print(listofreceptors)
        listofreceptorstemp = listofreceptors[receptor][13:]
        nomreceptor = listofreceptorstemp[:-6]
        receptorname = nomreceptor
        adressereceptor = cwd + "receptors/"
        path_receptor = adressereceptor + nomreceptor + ".pdbqt"
        dirmap = dirmaps[receptor]
        os.chdir(cwd)

        if software == "VINA" or software == "SMINA" or software == "QVINA":
            conftxtcheck = dirmap + receptorname + ".txt"  # AV
            # print(conftxtcheck)  # AV

            if (os.path.isfile(conftxtcheck)) == False:  # AV
                vcc.createconf(
                    nptsx,
                    nptsy,
                    nptsz,
                    gridcenterx,
                    gridcentery,
                    gridcenterz,
                    spacing,
                    path_receptor,
                    receptorname,
                )  # AV

        # ligandfolder = "outputfile"+str(ligandnumber)
        # ligandslices = [secondpathdb, ligandfolder]
        pathdb2 = currentligand[: currentligand.rfind("/")] + "/"

        # ligandfilename = ""
        # ligandfiletotal = ""
        # ligandfiletotal, ligandfilename = find.findpdbqt(ligandnumber, pathdb)
        # ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)

        path_ligand, pathligand, nameligand = edit.editligandpdbqt(
            software,
            currentligand,
            receptorname,
            dossiertemps,
            ligandfilename,
            cwd,
            ligandfirstpath,
        )
        # a changer pour une position dependante de l'emplacement spécifié par l'utilisateur
        dpflocation = path_ligand + "DOCKING.dpf"

        if DEBUG_FLAG == True:
            print("Software:")
            print(software)
            print("ligandfiletotal")
            print(currentligand)
            print("path ligand")
            print(pathligand)
            print("receptor:")
            print(nomreceptor)
            print("path db")
            print(pathdb)
            print("dir maps:")
            print(dirmap)

        if software == "GPU" or software == "AD4":
            ligandtype = dpf.dpfcreation(
                pathligand,
                path_receptor,
                dpflocation,
                dirmap,
                cwd,
                nomreceptor,
                software,
            )
            # print("ligand type: ")
            # print(ligandtype)
            if software == "GPU":
                fld.fldcreation(
                    ligandtype,
                    dirmap,
                    path_ligand,
                    gridcenterx,
                    gridcentery,
                    gridcenterz,
                    cwd,
                    nomreceptor,
                    nptsx,
                    nptsy,
                    nptsz,
                    spacing,
                )
            elif software == "AD4":
                fld2.fldcreation(
                    ligandtype,
                    dirmap,
                    path_ligand,
                    gridcenterx,
                    gridcentery,
                    gridcenterz,
                    cwd,
                    nomreceptor,
                    nptsx,
                    nptsy,
                    nptsz,
                    spacing,
                )

        # launching Autodock-VINA
        if software == "VINA":
            pathout = path_ligand + "out.pdbqt"
            if (os.path.isfile(pathout)) == False:
                if DEBUG_FLAG == True:
                    cmdvina = f"{pathsoftware} --config {conftxtcheck} --ligand {pathligand} --out {path_ligand}out.pdbqt"

                    print(f"Commande vina: {cmdvina}")
                    os.system(cmdvina)
                    # os.system("%s --config %s --ligand %s --out %sout.pdbqt --log %slog.txt" %(pathsoftware,conftxtcheck, pathligand, path_ligand, path_ligand))

                if DEBUG_FLAG == False:
                    subprocess.run(
                        [
                            "%s" % pathsoftware,
                            "--config",
                            conftxtcheck,
                            "--ligand",
                            pathligand,
                            "--out",
                            "%sout.pdbqt" % path_ligand,
                            "--log",
                            "%slog.txt" % path_ligand,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
                    print("SUCCED %s" % ligandnumber - 1, end="")
                    # write.write("SUCCED %s\n" % ligandnumber)

        if software == "SMINA":
            pathout = path_ligand + "out.pdbqt"
            if (os.path.isfile(pathout)) == False:
                if DEBUG_FLAG == True:
                    cmdsmina = f"{pathsoftware} --config {conftxtcheck} --ligand {pathligand} --out {path_ligand}out.pdbqt --log {path_ligand}log.txt"

                    print(f"Commande smina: {cmdsmina}")
                    os.system(cmdsmina)
                    # os.system("%s --config %s --ligand %s --out %sout.pdbqt --log %slog.txt" %(pathsoftware,conftxtcheck, pathligand, path_ligand, path_ligand))

                if DEBUG_FLAG == False:
                    subprocess.run(
                        [
                            "%s" % pathsoftware,
                            "--config",
                            conftxtcheck,
                            "--ligand",
                            pathligand,
                            "--out",
                            "%sout.pdbqt" % path_ligand,
                            "--log",
                            "%slog.txt" % path_ligand,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
                    print("SUCCED %s" % ligandnumber - 1, end="")

        if software == "QVINA":
            pathout = path_ligand + "out.pdbqt"
            if (os.path.isfile(pathout)) == False:
                if DEBUG_FLAG == True:
                    cmdqvina = f"{pathsoftware} --config {conftxtcheck} --ligand {pathligand} --out {path_ligand}out.pdbqt --log {path_ligand}log.txt"

                    print(f"Commande qvina: {cmdqvina}")
                    os.system(cmdqvina)
                    # os.system("%s --config %s --ligand %s --out %sout.pdbqt --log %slog.txt" %(pathsoftware,conftxtcheck, pathligand, path_ligand, path_ligand))

                if DEBUG_FLAG == False:
                    subprocess.run(
                        [
                            "%s" % pathsoftware,
                            "--config",
                            conftxtcheck,
                            "--ligand",
                            pathligand,
                            "--out",
                            "%sout.pdbqt" % path_ligand,
                            "--log",
                            "%slog.txt" % path_ligand,
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
                    print("SUCCED %s" % ligandnumber - 1, end="")

        os.chdir(path_ligand)

        # launching Autodock-GPU
        if software == "GPU" or software == "AD4":
            numberofruns = nruns
            # print("dpflocation: ")
            # print(dpflocation)
            if DEBUG_FLAG == True:
                if software == "GPU":
                    runautodock = (
                        pathsoftware
                        + " --import_dpf "
                        + dpflocation
                        + " --nrun "
                        + numberofruns
                        + " --gbest 1"
                    )
                    os.system(runautodock)

            pathbest = path_ligand + "best.pdbqt"
            if (os.path.isfile(pathbest)) == False:
                if DEBUG_FLAG == True:
                    if software == "GPU":
                        runautodock = (
                            pathsoftware
                            + " --import_dpf "
                            + dpflocation
                            + " --nrun "
                            + numberofruns
                            + " --gbest 1"
                        )
                        os.system(runautodock)
                    if software == "AD4":
                        runautodock = (
                            pathsoftware
                            + " -p "
                            + dpflocation
                            + " -l "
                            + pathligand
                            + "log.txt"
                        )
                        os.system(runautodock)

                if DEBUG_FLAG == False:
                    subprocess.run(
                        [
                            "%s" % pathsoftware,
                            "--import_dpf",
                            dpflocation,
                            "--nrun",
                            numberofruns,
                            "--gbest",
                            "1",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                    )
                    print("SUCCED %s" % ligandnumber - 1, end="")
                    # write.write("SUCCED %s\n" % ligandnumber)

        if software == "GNINA":
            # ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)
            if DEBUG_FLAG == True:
                rungnina = f"{pathsoftware} -r {path_receptor} -l {currentligand} -o {path_ligand}out.pdbqt --center_x {gridcenterx} --center_y {gridcentery} --center_z {gridcenterz} --size_x {nptsx} --size_y {nptsy} --size_z {nptsz} --log {path_ligand}out.log  "
                os.system(rungnina)

            if DEBUG_FLAG == False:
                rungnina = f"{pathsoftware} -r {path_receptor} -l {currentligand} -o {path_ligand}out.pdbqt --center_x {gridcenterx} --center_y {gridcentery} --center_z {gridcenterz} --size_x {nptsx} --size_y {nptsy} --size_z {nptsz} --log {path_ligand}out.log  "
                os.system(rungnina)
                # gd.dock_ligand(receptor,currentligand,path_ligand)

        """
        except:

            print("FAILED %s"%ligandnumber)
            #write.write("FAILED %s\n"%ligandnumber)

            Failed=ligandnumber

           pass
        """

    liganddocktime2 = time.time()
    liganddocktimetotal = liganddocktime2 - liganddocktime1
    print(
        "temps de dock %s secondes, ligand: %s"
        % (liganddocktimetotal, ligandfirstpath),
        end="",
    )
    Failed = ligandnumber
    return Failed
