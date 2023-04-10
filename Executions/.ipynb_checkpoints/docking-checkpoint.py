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
import multiprocessing as mp
import glob
import convertsdf as csdf
import os.path
import createmaps2 as cm
from tqdm import tqdm
import argparse
import gninadock as gd
def docking(software:str,nptsx:str,nptsy:str,nptsz:str,gridcenterx:str,gridcentery:str,gridcenterz:str,spacing:str,threads:str,nruns:str,pathdb:str,DEBUG_FLAG:bool,listofpdbqt:list,dossiertemps:str,listofreceptors:list,dirmaps:list,cwd:str,pathsoftware:str,ligandnumber):
    #print(FAIL)

    # Full path
    currentligand = listofpdbqt[ligandnumber]
    ligandfilename = currentligand.split("/")[-1] #outputfile34.pdbqt

    ligandfirstpath = currentligand.split("/")[-1][:-6] # outputfile34
    #ligandfirstpath = "outputfile"+str(ligandnumber)

    # print(ligandfirstpath)
    liganddocktime1 = time.time()

    # Execution du docking sur chacun des recepteurs
    for receptor in range(len(listofreceptors)):
        #try:
        Failed = False
        # print(listofreceptors)
        listofreceptorstemp = listofreceptors[receptor][13:]
        nomreceptor = listofreceptorstemp[:-6]
        receptorname = nomreceptor
        adressereceptor = cwd+"receptors/"
        path_receptor = adressereceptor + nomreceptor + ".pdbqt"
        dirmap = dirmaps[receptor]
        os.chdir(cwd)

        if software == "VINA":
            conftxtcheck = dirmap+receptorname+".txt"  # AV
            #print(conftxtcheck)  # AV

            if (os.path.isfile(conftxtcheck)) == False:  # AV
                vcc.createconf(nptsx, nptsy, nptsz, gridcenterx, gridcentery,
                            gridcenterz, spacing, path_receptor, receptorname)  # AV

        #ligandfolder = "outputfile"+str(ligandnumber)
        #ligandslices = [secondpathdb, ligandfolder]
        pathdb2 = currentligand[:currentligand.rfind("/")]+"/"

        #ligandfilename = ""
        #ligandfiletotal = ""
        #ligandfiletotal, ligandfilename = find.findpdbqt(ligandnumber, pathdb)
        #ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)

        path_ligand, pathligand, nameligand = edit.editligandpdbqt(
                software,currentligand, receptorname, dossiertemps, ligandfilename, cwd, ligandfirstpath)
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

        if software == "GPU":
            ligandtype = dpf.dpfcreation(
                pathligand, path_receptor, dpflocation, dirmap, cwd, nomreceptor)
        #print("ligand type: ")
        # print(ligandtype)
            fld.fldcreation(ligandtype, dirmap, path_ligand, gridcenterx,
                        gridcentery, gridcenterz, cwd, nomreceptor, nptsx, nptsy, nptsz)

        #launching Autodock-VINA
        if software == "VINA":
            pathout = path_ligand+"out.pdbqt"
            if (os.path.isfile(pathout)) == False:
                if DEBUG_FLAG == True:
                    cmdvina = f"{pathsoftware} --config {conftxtcheck} --ligand {pathligand} --out {path_ligand}out.pdbqt --log {path_ligand}log.txt"
                    
                    print(f"Commande vina: {cmdvina}")
                    os.system(cmdvina)
                    #os.system("%s --config %s --ligand %s --out %sout.pdbqt --log %slog.txt" %(pathsoftware,conftxtcheck, pathligand, path_ligand, path_ligand))


                if DEBUG_FLAG == False:
                    subprocess.run(
                    [
                    "%s" % pathsoftware,
                    "--config",
                    conftxtcheck,
                    "--ligand",
                    pathligand,
                    "--out",
                    "%sout.pdbqt"%path_ligand,
                    "--log",
                    "%slog.txt"%path_ligand,
                    ],
                        stderr=open(os.devnull, "wb")
                    )
                    print("SUCCED %s" % ligandnumber,end='')
                    fwrite.write("SUCCED %s\n" % ligandnumber)


        os.chdir(path_ligand)

        #launching Autodock-GPU
        if software == "GPU":
            #print("dpflocation: ")
            # print(dpflocation)
            if DEBUG_FLAG == True:
                runautodock = pathsoftware + " --import_dpf "+dpflocation+" --gbest 1"
                os.system(runautodock)

            pathbest = path_ligand+"best.pdbqt"
            if (os.path.isfile(pathbest)) == False:

                if DEBUG_FLAG == True:
                    runautodock = pathsoftware + " --import_dpf "+dpflocation+" --nrun "+numberofruns+" --gbest 1"
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
                        stdout=open(os.devnull, "wb"),
                    )
                    print("SUCCED %s" % ligandnumber,end='')
                    fwrite.write("SUCCED %s\n" % ligandnumber)

        if software == "GNINA":
            #ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)
            if DEBUG_FLAG == True:
                rungnina = f"{pathsoftware} -r {rec_file} -l {lig_file} -o {output_file} --center_x {gridcenterx} --center_y {gridcentery} --center_z {gridcenterz} --size_x {nptsx} --size_y {nptsy} --size_z {nptsz} "
                os.system(cmd)

            if DEBUG_FLAG == False:
                gd.dock_ligand(receptor,currentligand,path_ligand)





        """
        except:

            print("FAILED %s"%ligandnumber)
            #write.write("FAILED %s\n"%ligandnumber)

            Failed=ligandnumber

           pass
        """


    liganddocktime2 = time.time()
    liganddocktimetotal = liganddocktime2 - liganddocktime1
    print("temps de dock %s secondes, ligand: %s" %
            (liganddocktimetotal, ligandfirstpath),end='')
    return Failed