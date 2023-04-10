import os, shutil
import subprocess
def editligandpdbqt(software,currentligand, receptorname, dossiertemps, ligandfilename, cwd, ligandfirstpath):
    ligandpdb = currentligand
    nameligand = ligandfilename
    #print("nameligand: ")
    #print(ligandfilename)
    #print("ligandfirstpath: ")
    #print(ligandfirstpath)
    path_ligand1 = cwd + "results_"+software+"/DOCKED/"+ligandfirstpath+"/"
    #print(path_ligand1)
    if not os.path.exists(path_ligand1):
        os.makedirs(path_ligand1)
        #print("Directory " , path_ligand1 ,  " Created ")
    else:
        #print("echec")
        pass

    path_ligand = (
        cwd
        +"results_"+software+"/DOCKED/"
        +ligandfirstpath
        +"/"
        + receptorname
        + "_"
        + ligandfilename[:-6]
        + "_"
        + dossiertemps
        + "/"
    )
    #print(path_ligand)
    if not os.path.exists(path_ligand):
        os.makedirs(path_ligand)
        #print("Directory " , path_ligand ,  " Created ")
    else:
        #print("echec")
        pass
    liganddirpaste = path_ligand + nameligand 
    print("path ligand:" )
    print(path_ligand)
    print(" liganddirpaste : ")
    print(liganddirpaste)
    os.system('ln -sf %s %s'%(ligandpdb,liganddirpaste))
    #os.symlink('%s'%ligandpdb, '%s'%liganddirpaste)
    #shutil.copyfile(ligandpdb, liganddirpaste)
    return path_ligand, liganddirpaste, nameligand
