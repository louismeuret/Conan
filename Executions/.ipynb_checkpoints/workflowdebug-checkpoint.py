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

parser = argparse.ArgumentParser()
parser.add_argument('--useconfig', required=False)
args = vars(parser.parse_args())
nproc_paralelle = 1  #if you use GPU (e.g. autodockGPU, consider to add just a few amount of cores to not oversatured the GPU memory -e.g. nproc=6 for delavega workstation -kind of 24G GPU vram memory. Otherwise, just burn the microprocesor ;) -)

fwrite = open('logout.txt', 'w')

VINA_FLAG = True
AUTODOCK_GPU_FLAG = False
GNINA_FLAG = False
DEBUG_FLAG = True

# Make some test before to raach 100% GPU

#Executions parameters, if workflowdebug.py --useconfig yes, the config file will be used
nptsx = "90"
nptsy = "75"
nptsz = "85"

gridcenterx = "55"
gridcentery = "-21"
gridcenterz = "-20"

numberofruns = "100"

spacing = "0.375" #if only define the grid with autodock vina, the spacing is 1.0. Otherwise, use the autogrid spacing and editligandpdbqt will adapt to autodock vina dimension

cwd = os.getcwd()
cwd = cwd.replace("Executions", "")
dbused = "/home/louis/Téléchargements/Databases/Chimiothèques/ICSN/"
secondpathdb = "obabel"

autodock_executable = cwd+"parametres/executables/autodock_gpu_128wi"
vina_executable = cwd+"parametres/executables/vina"
gnina_executable = cwd+"Parametres/executables/gnina"


meilleureenergie = 0
meilleurligand = ""

softwareused = {"VINA":False,"GPU":False,"GNINA":False,"QVINA":False,"SMINA":False}

with open('../parametres/conanconfig.txt') as f:
    lines = f.readlines()


#if argument = yes, use of the conanconfig.txt
if args['useconfig'] == 'yes':
    print("HERE")
    for x in range(len(lines)):
        if lines[x].split(" ")[0] == "#SOFTWARE#":
            
            softwareused[lines[x].split(" ")[1].upper()] = True 
            """
            if lines[x].split(" ")[1] == "vina":
                VINA_FLAG = True
                AUTODOCK_GPU_FLAG = False
                GNINA_FLAG = False
            if lines[x].split(" ")[1] == "gpu":
                VINA_FLAG = False
                AUTODOCK_GPU_FLAG = True
                GNINA_FLAG = False
            if lines[x].split(" ")[1] == "gnina":
                VINA_FLAG = False
                AUTODOCK_GPU_FLAG = False
                GNINA_FLAG = True
            """

        if lines[x].split(" ")[0] == "#DEBUG#":
            if lines[x].split(" ")[1] == "yes":
                DEBUG_FLAG = True
            if lines[x].split(" ")[1] == "no":
                DEBUG_FLAG = False
                
        if lines[x].split(" ")[0] == "#THREADS#":
            nproc_paralelle = int(lines[x].split(" ")[1])

        if lines[x].split(" ")[0] == "#NRUNS#":
            numberofruns = int(lines[x].split(" ")[1])
            
        if lines[x].split(" ")[0] == "#PATHDB#":
            secondpathdb = lines[x].split(" ")[1].split("/")[-1]
            dbused = lines[x].split(" ")[1].replace(secondpathdb,"")
            
        if lines[x].split(" ")[0] == "#SPACING#":
            spacing = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#CENTERX#":
            gridcenterx = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#CENTERY#":
            gridcentery = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#CENTERZ#":
            gridcenterz = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#SIZEX#":
            nptsx = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#SIZEY#":
            nptsy = lines[x].split(" ")[1]
        if lines[x].split(" ")[0] == "#SIZEZ#":
            nptsz = lines[x].split(" ")[1]


def softwareset():
    return str(list(softwareused.keys())[list(softwareused.values()).index(True)])
startofdock = time.time()

#receptorname = "receptor_multimer"
#nomreceptor = receptorname

#list all of the pdbqt present in the db folder, to set the number of ligand to dock
pathdbpdbqt = dbused + secondpathdb + "/**/*.pdbqt" 
listofpdbqt = glob.glob(pathdbpdbqt)
numberofligandtodock = len(listofpdbqt)
countligand = 1
numberofreceptor = 5


listofreceptors = glob.glob('../receptors/*.pdbqt')


dirmaps = cm.create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, listofreceptors)

def docking(ligandnumber):
    software = str(softwareset())
    print(software)
    #print(FAIL)
        
    ligandfirstpath = "outputfile"+str(ligandnumber)
    # print(ligandfirstpath)
    liganddocktime1 = time.time()
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

        ligandfolder = "outputfile"+str(ligandnumber)
        ligandslices = [secondpathdb, ligandfolder]
        pathdb = dbused + ligandslices[0] + "/" + ligandslices[1] + "/"

        ligandfilename = ""
        ligandfiletotal = ""
        ligandfiletotal, ligandfilename = find.findpdbqt(ligandnumber, pathdb)
        #ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)

        path_ligand, pathligand, nameligand = edit.editligandpdbqt(
                software,ligandfiletotal, receptorname, ligandslices, ligandfilename, cwd, ligandfirstpath)
        dpflocation = path_ligand + "DOCKING.dpf"

        if DEBUG_FLAG == True:
            print("Software:")
            print(software)
            print("ligandfiletotal")
            print(ligandfiletotal)
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
                    os.system("%s --config %s --ligand %s --out %sout.pdbqt --log %slog.txt" %(vina_executable,conftxtcheck, pathligand, path_ligand, path_ligand))
                    
                
                if DEBUG_FLAG == False:
                    subprocess.run(
                    [
                    "%s" % vina_executable,
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
                runautodock = autodock_executable + " --import_dpf "+dpflocation+" --gbest 1"
                os.system(runautodock)
                
            pathbest = path_ligand+"best.pdbqt"
            if (os.path.isfile(pathbest)) == False:
                
                if DEBUG_FLAG == True:
                    runautodock = autodock_executable + " --import_dpf "+dpflocation+" --nrun "+numberofruns+" --gbest 1"
                    os.system(runautodock)
                if DEBUG_FLAG == False:
                    subprocess.run(
                        [
                            "%s" % autodock_executable,
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
            ligandfiletotal = csdf.convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd)
            gd.dock_ligand(receptor,ligandfiletotal,path_ligand)



            
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


# paralellization
file_ligands = np.arange(1, numberofligandtodock, 1)
p = mp.Pool(nproc_paralelle)  # mp.cpu_count())
FAIL = list(tqdm(p.imap_unordered(docking, [x for x in file_ligands]),total=numberofligandtodock))
p.close()
